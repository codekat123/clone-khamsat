from django.db import models
from user_profile.models import BuyerProfile
from services.models import Service
from django.core.validators import MinValueValidator,MaxValueValidator



class Rating(models.Model):
     user = models.ForeignKey(BuyerProfile,on_delete=models.CASCADE,related_name='user_rate')
     service = models.ForeignKey(Service,on_delete=models.CASCADE,related_name='service_rate')
     comment = models.TextField(max_length=500)
     stars = models.PositiveIntegerField(default=0,validators=[MinValueValidator(0),MaxValueValidator(5)])
     