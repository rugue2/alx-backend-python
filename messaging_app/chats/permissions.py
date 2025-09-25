from rest_framework import permissions

class IsMessageParticipant(permissions.BasePermission):
    """
    Custom permission to only allow participants of a message to view it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed if the user is a participant in the message
        return request.user in [obj.sender, obj.recipient]

class IsConversationParticipant(permissions.BasePermission):
    """
    Custom permission to only allow participants of a conversation to view it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed if the user is a participant in the conversation
        return request.user in [obj.user1, obj.user2]