"""
Test suite for the Category model and views.
Covers creation, listing, updating, deletion, and access control.
"""

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Category


class CategoryTests(APITestCase):
    """
    Test cases for the Category model and API views.
    """

    def setUp(self):
        """
        Create test users and categories.
        """
        self.user1 = User.objects.create_user(username="user1", password="pass1234")
        self.user2 = User.objects.create_user(username="user2", password="pass1234")

        self.category1 = Category.objects.create(
            name="Work",
            description="Work related notes",
            color="#ff0000",
            owner=self.user1,
        )

        self.category2 = Category.objects.create(
            name="Personal",
            description="Personal notes",
            color="#00ff00",
            owner=self.user2,
        )

        self.client.login(username="user1", password="pass1234")

    def test_list_categories_returns_only_user_owned(self):
        """
        Ensure user only sees their own categories.
        """
        response = self.client.get(reverse("category-list-create"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "Work")

    def test_create_category_successfully(self):
        """
        Ensure a user can create a category.
        """
        data = {
            "name": "New Category",
            "description": "Test description",
            "color": "#123456"
        }
        response = self.client.post(reverse("category-list-create"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.filter(owner=self.user1).count(), 2)

    def test_retrieve_category(self):
        """
        Ensure a user can retrieve their category.
        """
        url = reverse("category-detail", args=[self.category1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Work")

    def test_retrieve_other_user_category_forbidden(self):
        """
        Ensure a user cannot retrieve someone else's category.
        """
        url = reverse("category-detail", args=[self.category2.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_category(self):
        """
        Ensure a user can update their category.
        """
        url = reverse("category-detail", args=[self.category1.id])
        data = {
            "name": "Updated Name",
            "description": "Updated description",
            "color": "#654321"
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.category1.refresh_from_db()
        self.assertEqual(self.category1.name, "Updated Name")

    def test_delete_category(self):
        """
        Ensure a user can delete their category.
        """
        url = reverse("category-detail", args=[self.category1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Category.objects.filter(id=self.category1.id).exists())

    def test_unauthenticated_user_denied(self):
        """
        Ensure unauthenticated users cannot access category endpoints.
        """
        self.client.logout()
        response = self.client.get(reverse("category-list-create"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
