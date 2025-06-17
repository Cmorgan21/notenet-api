from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from profiles.models import Profile
from .models import Note
from .serializers import UserSerializer, NoteSerializer


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


class NoteList(generics.ListAPIView):
    """
    Allows authenticated users with a token to see their notes
    """
    permission_classes = [IsAuthenticated]
    serializer_class = NoteSerializer

    def get_queryset(self):
        return (
            Note.objects
            .filter(author=self.request.user)
            .order_by('-created_on')
        )


class CreateNoteView(generics.CreateAPIView):
    """
    Allows authenticated users with a token to create a note
    """
    permission_classes = [IsAuthenticated]
    serializer_class = NoteSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context


class NoteDetail(generics.RetrieveAPIView):
    """
    Allows authenticated users with a token to see their notes
    """
    permission_classes = [IsAuthenticated]
    serializer_class = NoteSerializer

    def get_queryset(self):
        return Note.objects.filter(author=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        note = get_object_or_404(queryset, pk=kwargs['pk'])
        serializer = self.get_serializer(note)
        return Response(serializer.data)


class UpdateNoteView(generics.UpdateAPIView):
    """
    Allows authenticated users with a token to update a note
    """
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Note.objects.filter(author=self.request.user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})  # Pass request to serializer
        return context


class DeleteNoteView(generics.DestroyAPIView):
    """
    Allows authenticated users with a token to delete a note
    """
    permission_classes = [IsAuthenticated]
    serializer_class = NoteSerializer

    def get_queryset(self):
        return Note.objects.filter(author=self.request.user)
