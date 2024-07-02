from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    """
    A model representing a user profile
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    image = models.ImageField(default='../default_profile_lyli1b', upload_to='images/')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """
        Meta class for the Profile model
        """
        ordering = ['-created_at']

    def __str__(self):
        """
        String representation of the Profile model
        """
        return f"Profile for {self.user.username}"

