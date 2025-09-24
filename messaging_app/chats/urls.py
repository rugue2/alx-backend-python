from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import ConversationViewSet, MessageViewSet

# Initialize the router
router = routers.DefaultRouter()

# Register viewsets with the router
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')

# Define URL patterns
urlpatterns = [
    # Include the router URLs
    path('', include(router.urls)),
]