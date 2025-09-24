from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter conversations to only those the user is part of"""
        return self.queryset.filter(participants=self.request.user)

    def perform_create(self, serializer):
        """Create a new conversation and automatically add the creator as participant"""
        conversation = serializer.save()
        conversation.participants.add(self.request.user)

    @action(detail=True, methods=['post'])
    def add_participant(self, request, pk=None):
        """Add a participant to an existing conversation"""
        conversation = self.get_object()
        user_id = request.data.get('user_id')
        
        if not user_id:
            return Response(
                {'error': 'user_id is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        conversation.participants.add(user_id)
        return Response(
            ConversationSerializer(conversation).data,
            status=status.HTTP_200_OK
        )

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter messages to only those from conversations the user is part of"""
        conversation_id = self.request.query_params.get('conversation_id')
        queryset = self.queryset.filter(
            conversation__participants=self.request.user
        )
        
        if conversation_id:
            queryset = queryset.filter(conversation_id=conversation_id)
        
        return queryset

    def perform_create(self, serializer):
        """Create a new message with the current user as sender"""
        conversation_id = self.request.data.get('conversation_id')
        
        if not conversation_id:
            raise serializers.ValidationError(
                {'conversation_id': 'This field is required.'}
            )
            
        conversation = Conversation.objects.filter(
            id=conversation_id,
            participants=self.request.user
        ).first()
        
        if not conversation:
            raise serializers.ValidationError(
                {'conversation_id': 'Invalid conversation or not a participant.'}
            )
            
        serializer.save(
            sender=self.request.user,
            conversation=conversation
        )
