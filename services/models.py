from django.db import models
from user_profile.models import SellerProfile
from django.utils.text import slugify




class Category(models.Model):
    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=100,unique=True)

    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args,**kwargs)

    def __str__(self):
       return self.name
            
            



class Service(models.Model):

    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(Category,on_delete=models.SET_NULL,null=True,blank=True,related_name='services')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_time = models.PositiveIntegerField(help_text="Delivery time in days")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    freelancer = models.ForeignKey(SellerProfile,on_delete=models.CASCADE,related_name='services')
    is_active = models.BooleanField(default=False)
    rating = models.FloatField(default=0.0)
    orders_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title
    
    def save(self,*args,**kwargs):
        if not self.slug:
          unique_slug = slugify(self.title)
          slug = unique_slug
          count = 1
          while Service.objects.filter(slug=slug).exists():
              slug = f"{slug}-{count}"
              count += 1
          self.slug = slug
          super().save(*args,**kwargs)
