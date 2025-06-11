from rest_framework import serializers
from .models import Category

class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for Category model.
    """
    class Meta:
        model = Category
        fields = ['id', 'name', 'owner', 'description', 'color', 'created_on']
        read_only_fields = ['owner', 'created_on']
