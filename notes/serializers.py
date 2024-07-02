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

    def create(self, validated_data):
        try:
            user = User.objects.create_user(
                username=validated_data['username'],
                email=validated_data['email'],
                password=validated_data['password']
            )
            Profile.objects.create(user=user, name=user.username, email=user.email)
            return user
        except ValidationError as e:
            raise serializers.ValidationError({'detail': str(e)})
        except Exception as e:
            raise serializers.ValidationError({'detail': str(e)})

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        instance = super().update(instance, validated_data)
        if password:
            instance.set_password(password)
            instance.save()
        return instance

class NoteSerializer(serializers.ModelSerializer):
    """
    Serializes all fields of Note Model
    Excludes author field from being manipulated
    """
    class Meta:
        """
        Meta class for the NoteSerializer
        """
        model = Note
        fields = ['id', 'title', 'body', 'created_on', 'updated_at']
        extra_kwargs = {'author': {'read_only': True}}

    