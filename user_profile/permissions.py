from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsSeller(BasePermission):
     def has_permission(self,request,view):
          return request.user.is_authenticated and hasattr(request.user,'seller_profile')
     def has_object_permission(self,request,view,obj):
          return obj.seller_profile.user == request.user

class IsBuyer(BasePermission):
     def has_permission(self,request,view):
          return request.user.is_authenticated and hasattr(request.user,'buyer_profile')
     def has_object_permission(self,request,view,obj):
          return obj.buyer_profile.user == request.user

class IsAdmin(BasePermission):
     def bas_permission(self,request,view):
          return request.user and request.user.is_staff