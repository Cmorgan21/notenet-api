from rest_framework import generics, permissions
from .models import Category
from .serializers import CategorySerializer

class CategoryListCreateView(generics.ListCreateAPIView):
    """
    List all categories or create a new category.
    """
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Category.objects.filter(owner=self.request.user).order_by('-created_on')

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)