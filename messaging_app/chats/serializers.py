from rest_framework import serializers
from .models import User, Conversation, Message

class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='get_full_name', read_only=True)
    
    class Meta:
        model = User
        fields = ['user_id', 'username', 'email', 'first_name', 'last_name', 
                 'phone_number', 'role', 'created_at', 'full_name']
        read_only_fields = ['user_id', 'created_at']

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    
    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'message_body', 'sent_at']
        read_only_fields = ['message_id', 'sent_at']

class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)
    last_message = serializers.SerializerMethodField()
    participant_count = serializers.SerializerMethodField()
    conversation_title = serializers.CharField(source='__str__', read_only=True)
    participant_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        write_only=True,
        queryset=User.objects.all(),
        source='participants'
    )

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'messages', 
                 'participant_ids', 'created_at']
        read_only_fields = ['conversation_id', 'created_at']

    def validate_participant_ids(self, value):
        if len(value) < 2:
            raise serializers.ValidationError(
                "A conversation must have at least 2 participants"
            )
        return value

    def get_last_message(self, obj):
        """Get the most recent message in the conversation"""
        last_message = obj.messages.order_by('-sent_at').first()
        if last_message:
            return MessageSerializer(last_message).data
        return None

    def get_participant_count(self, obj):
        """Get the number of participants in the conversation"""
        return obj.participants.count()