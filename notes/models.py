from django.db import models
from django.contrib.auth.models import User
from categories.models import Category

# Create your models here.

class Note(models.Model):
    """
    A model representing a note
    """
    title = models.CharField(max_length=100)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='notes')  # ✅ New field

    def __str__(self):
        return f'{self.title} by {self.author}'

