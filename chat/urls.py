from django.urls import path
from .views import ConversationAPIView,Room


app_name = 'chat'


urlpatterns = [
     path('conversation/<user_id>/',ConversationAPIView.as_view,name='conversation'),
     path('room/<conversation_id>/',Room.as_view(),name='Room'),
]