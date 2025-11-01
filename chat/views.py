from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Conversation
from .serializers import ConversationSerializer,MessageSerializer
from rest_framework.generics import ListAPIView

User = get_user_model()

class ConversationAPIView(APIView):
    def post(self, request):
        try:
            other_id = request.data.get('user_id')
            if not other_id:
                return Response({'message': 'Missing user ID'}, status=status.HTTP_400_BAD_REQUEST)

            other = User.objects.get(id=other_id)
            me = request.user

            if (me.is_buyer and other.is_buyer) or (me.is_seller and other.is_seller):
                return Response({'message': 'You are not allowed to talk to each other.'},
                                status=status.HTTP_403_FORBIDDEN)


            buyer, seller = (me, other) if me.is_buyer else (other, me)


            conversation, created = Conversation.objects.get_or_create(buyer=buyer, seller=seller)
            serializer = ConversationSerializer(conversation)

            return Response({
                'message': 'New conversation created' if created else 'Existing conversation found',
                'conversation': serializer.data
            }, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class Room(APIView):
    def get(self, request, conversation_id):
        try:
            conversation = Conversation.objects.get(id=conversation_id)

            if request.user.id not in (conversation.buyer.id, conversation.seller.id):
                return Response(
                    {"error": "You're not part of this conversation."},
                    status=status.HTTP_403_FORBIDDEN
                )

            messages = (
                conversation.messages
                .select_related('sender')
                .order_by('-created_at')[:30]
            )

            serializer = MessageSerializer(messages, many=True)

            return Response(
                {"messages": serializer.data},
                status=status.HTTP_200_OK
            )

        except Conversation.DoesNotExist:
            return Response(
                {"error": "Conversation not found."},
                status=status.HTTP_404_NOT_FOUND
            )