from rest_framework.generics import CreateAPIView
from .utils import verify_otp,generate_otp,store_otp
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer , VerifyOTPSerializer , ResendOTPSerializer
from .tasks import send_otp_email
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken, TokenError


User = get_user_model()

class RegisterAPIView(CreateAPIView):
    serializer_class = RegisterSerializer
    authentication_classes = []  
    permission_classes = []      

    def perform_create(self, serializer):
        user = serializer.save(is_active=False)  
        send_otp_email(user.email)

    def create(self, request, *args, **kwargs):
        """
        Overriding create() to customize the response message
        after user registration and OTP sending.
        """
        response = super().create(request, *args, **kwargs)
        return Response(
            {
                "message": "User created successfully. Please check your email for the OTP.",
                "email": response.data.get("email"),
            },
            status=status.HTTP_201_CREATED,
        )


class VerifyOTPAPIView(APIView):
    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        otp = serializer.validated_data['otp']

        if verify_otp(email, otp):
            user = User.objects.filter(email=email).first()
            if user:
                user.is_active = True
                user.save()
                return Response({"message": "Account verified successfully."}, status=200)
            return Response({"message": "User not found."}, status=404)

        return Response({"message": "Invalid or expired OTP."}, status=400)
            

class ResendOTPAPIView(APIView):
    def post(self, request):
        serializer = ResendOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        user = User.objects.filter(email=email).first()
        if not user:
            return Response(
                {'message': 'User not found.'},
                status=status.HTTP_404_NOT_FOUND
            )

        send_otp_email(email)
        return Response(
            {'message': 'OTP sent to your email successfully.'},
            status=status.HTTP_200_OK
        )  




class LogoutAPIView(APIView):
    
    def post(self,request):
        try:
            refresh_token = request.data.get('refresh_token')
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message":"logout successful"},status=status.HTTP_205_RESET_CONTENT)
        except TokenError:
            return Response({"message":"Invalid Token"},status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
            return Response({"error": "Refresh token required."}, status=status.HTTP_400_BAD_REQUEST)


