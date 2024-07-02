from rest_framework import serializers
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for the Profile model
    """
    class Meta:
        """
        Meta class for the Profile model
        """
        model = Profile
        fields = ['id', 'user', 'name', 'email', 'image', 'created_at']
        read_only_fields = ['user', 'created_at']

