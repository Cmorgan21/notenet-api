from django.test import TestCase
from django.contrib.auth.models import User
from .models import Profile

class ProfileModelTest(TestCase):
    """
    Test cases for the Profile model
    """

    def setUp(self):
        """
        Create a user instance
        """
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='password123')
        Profile.objects.create(user=self.user, email=self.user.email)

    def test_profile_creation(self):
        """
        Test that the Profile instance is created when the User is created
        """
        self.assertTrue(Profile.objects.filter(user=self.user).exists())
        profile = Profile.objects.get(user=self.user)
        profile.name = self.user.username
        profile.save()
        self.assertEqual(profile.name, self.user.username)
        self.assertEqual(profile.email, self.user.email)

    def test_profile_update(self):
        """
        Test that the Profile instance is updated when the User is updated
        """
        self.user.username = 'updated_user'
        self.user.email = 'updateduser@example.com'
        self.user.save()

        profile = Profile.objects.get(user=self.user)
        profile.name = self.user.username
        profile.email = self.user.email
        profile.save()

        self.assertEqual(profile.name, 'updated_user')
        self.assertEqual(profile.email, 'updateduser@example.com')
