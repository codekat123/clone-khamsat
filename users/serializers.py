from rest_framework import serializers 
from .models import User


class RegisterSerializer(serializers.ModelSerializer):
     
     class Meta:
          model = User
          fields = ['first_name','last_name','username','email','password','role']
     
     def save(self, **kwargs):
         password = self.validated_data.pop('password')
         user = User.objects.create(
             **self.validated_data
         )
         user.set_password(password)
         user.save()
         self.user = user
         return user
     
class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)



class ResendOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()