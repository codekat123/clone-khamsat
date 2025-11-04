from rest_framework import serializers 
from .models import User



class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password', 'role']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self, **kwargs):
        password = self.validated_data.pop('password')
        email = self.validated_data.get('email')
        username = self.validated_data.get('username')

        user = User.objects.create_user(
            email=email,
            username=username,
            password=password,
            **self.validated_data
        )
        return user
     
class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)



class ResendOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()