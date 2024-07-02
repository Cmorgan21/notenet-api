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

def create_or_update_profile(sender, instance, created, **kwargs):
    """
    Create or update a Profile instance when a User instance is created or updated
    """
    if created:
        # User instance is created, create a new profile
        Profile.objects.create(user=instance, name=instance.username, email=instance.email)
    else:
        # User instance is updated, get existing profile or create if it doesn't exist
        profile, _ = Profile.objects.get_or_create(user=instance)
        profile.name = instance.username
        profile.email = instance.email 
        profile.save()

