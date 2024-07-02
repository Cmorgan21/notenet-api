from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from rest_framework import serializers
from profiles.models import Profile
from .models import Note



class UserSerializer(serializers.ModelSerializer):
    """
    Serializes all fields of User Model
    Excludes password field from being manipulated
    """

    class Meta:
        """
        Meta class for the UserSerializer
        """
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}


    