from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from rest_framework import serializers
from profiles.models import Profile
from .models import Note, Category


class UserSerializer(serializers.ModelSerializer):
    """
    Serializes all fields of User Model
    Excludes password field from being manipulated
    """

    class Meta:
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


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'color', 'owner']


class NoteSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.none(),
        write_only=True,
        source='category',
        allow_null=True,
        required=False
    )

    class Meta:
        model = Note
        fields = ['id', 'title', 'body', 'created_on', 'updated_at', 'category', 'category_id']
        extra_kwargs = {'author': {'read_only': True}}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request', None)
        if request and hasattr(request, "user"):
            # Filter categories by owner == current user
            self.fields['category_id'].queryset = Category.objects.filter(owner=request.user)
