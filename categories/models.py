from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    """
    A model representing a catergory
    """
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categories')
    created_on = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)
    color = models.CharField(max_length=7, default="#ffffff")

    def __str__ (self):
        return f'{self.name}'
