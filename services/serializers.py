from rest_framework import serializers
from .models import Category, Service

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'title', 'price', 'slug']
        read_only_fields = ['slug']


class CategorySerializer(serializers.ModelSerializer):


    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'services']
        read_only_fields = ['slug']
