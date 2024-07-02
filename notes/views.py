from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from profiles.models import Profile
from .models import Note
from .serializers import UserSerializer, NoteSerializer

# Create your views here.

class CreateUserView(generics.CreateAPIView):
    """
    Allows anyone to create a user
    """
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        try:
            user = serializer.save()
            Profile.objects.get_or_create(user=user)
        except ValidationError as e:
            raise ValidationError({'detail': e.detail})
        except Exception as e:
            raise ValidationError({'detail': str(e)})