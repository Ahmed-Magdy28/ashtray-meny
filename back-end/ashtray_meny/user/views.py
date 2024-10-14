from rest_framework import generics, permissions
from user.serializers import UserSerializer
from rest_framework.response import Response
from rest_framework.views import APIView


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system."""
    serializer_class = UserSerializer


class ManageUserView(APIView):
    """Manage the authenticated user."""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """Retrieve the authenticated user."""
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
