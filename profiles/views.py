from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from .models import Profile
from .serializers import ProfileSerializer
from .serializers import ChangePasswordSerializer

class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, queryset=None):
        """
        Get the authenticated user.
        """
        return self.request.user
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        """
        Update the authenticated user's password.
        """
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.object.set_password(serializer.validated_data['password'])
            self.object.save()
            return Response({"status": "password set"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
