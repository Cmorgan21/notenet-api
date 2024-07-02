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


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for changing password
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        """
        Validate the new password
        """
        if value == self.context['request'].user.username:
            raise serializers.ValidationError("The new password must be different from the old password.")
        if len(value) < 8:
            raise serializers.ValidationError("The new password must be at least 8 characters long.")
        # You can also add more complex validations like checking for special characters, numbers, etc.
        return value

    def validate(self, attrs):
        """
        Validate the old password
        """
        user = self.context['request'].user
        if not user.check_password(attrs.get('old_password')):
            raise serializers.ValidationError({"old_password": "Old password is not correct"})
        return attrs