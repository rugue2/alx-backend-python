from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Conversation, Message

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'created_at')
    list_filter = ('role', 'created_at')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-created_at',)

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('conversation_id', 'created_at', 'get_participants')
    list_filter = ('created_at',)
    search_fields = ('conversation_id',)
    ordering = ('-created_at',)

    def get_participants(self, obj):
        return ", ".join([user.username for user in obj.participants.all()])
    get_participants.short_description = 'Participants'

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('message_id', 'sender', 'conversation', 'sent_at')
    list_filter = ('sent_at', 'sender')
    search_fields = ('message_body',)
    ordering = ('-sent_at',)
