"""
Views for user registration and note management.

Includes:
- User creation with automatic profile creation.
- Authenticated CRUD operations for notes.
"""

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError as DjangoValidationError
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from profiles.models import Profile
from .models import Note
from .serializers import UserSerializer, NoteSerializer


class CreateUserView(generics.CreateAPIView):
    """
    View to allow anyone to register a new user account.
    """
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        """
        Create a user and associated profile.
        """
        try:
            user = serializer.save()
            Profile.objects.get_or_create(user=user)
        except DjangoValidationError as err:
            raise DjangoValidationError({'detail': err.message})
        except Exception as err:
            raise DjangoValidationError({'detail': str(err)})


class NoteList(generics.ListAPIView):
    """
    View to list all notes for the authenticated user.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = NoteSerializer

    def get_queryset(self):
        """
        Return notes belonging to the requesting user.
        """
        return Note.objects.filter(author=self.request.user).order_by('-created_on')


class CreateNoteView(generics.CreateAPIView):
    """
    View to allow users to create a note.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = NoteSerializer

    def perform_create(self, serializer):
        """
        Save the new note with the current user as the author.
        """
        serializer.save(author=self.request.user)

    def get_serializer_context(self):
        """
        Add request context to the serializer for dynamic queryset filtering.
        """
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context


class NoteDetail(generics.RetrieveAPIView):
    """
    View to retrieve a single note by ID for the authenticated user.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = NoteSerializer

    def get_queryset(self):
        """
        Return notes owned by the current user.
        """
        return Note.objects.filter(author=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve the note instance and return serialized data.
        """
        queryset = self.get_queryset()
        note = get_object_or_404(queryset, pk=kwargs['pk'])
        serializer = self.get_serializer(note)
        return Response(serializer.data)


class UpdateNoteView(generics.UpdateAPIView):
    """
    View to update a note for the authenticated user.
    """
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Return only notes owned by the current user.
        """
        return Note.objects.filter(author=self.request.user)

    def get_serializer_context(self):
        """
        Add request to serializer context for filtered querysets.
        """
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context


class DeleteNoteView(generics.DestroyAPIView):
    """
    View to delete a note for the authenticated user.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = NoteSerializer

    def get_queryset(self):
        """
        Return only the notes of the authenticated user.
        """
        return Note.objects.filter(author=self.request.user)
