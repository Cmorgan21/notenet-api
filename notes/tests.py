from django.test import TestCase
from django.contrib.auth.models import User
from categories.models import Category
from .models import Note


class NoteModelTest(TestCase):
    """
    Test the Note model
    """

    def setUp(self):
        """
        Create test user, categories, and notes
        """
        self.user = User.objects.create_user(username='testuser', password='testpass')

        self.category = Category.objects.create(
            name='Work',
            owner=self.user,
            description='Work-related notes',
            color='#ffcc00'
        )

        self.note1 = Note.objects.create(
            title='Test Note 1',
            body='This is the body of test note 1.',
            author=self.user,
            category=self.category
        )

        self.note2 = Note.objects.create(
            title='Test Note 2',
            body='This is the body of test note 2.',
            author=self.user  # No category assigned
        )

    def test_note_creation(self):
        """
        Test if the Note model is created correctly
        """
        self.assertEqual(self.note1.title, 'Test Note 1')
        self.assertEqual(self.note1.body, 'This is the body of test note 1.')
        self.assertEqual(self.note1.author.username, 'testuser')
        self.assertEqual(self.note1.category.name, 'Work')

        self.assertEqual(self.note2.title, 'Test Note 2')
        self.assertEqual(self.note2.category, None)

    def test_note_str_method(self):
        """
        Test if the Note model __str__ method is working correctly
        """
        self.assertEqual(str(self.note1), 'Test Note 1 by testuser')
        self.assertEqual(str(self.note2), 'Test Note 2 by testuser')

    def test_note_auto_fields(self):
        """
        Test if the Note model auto fields are working correctly
        """
        self.assertIsNotNone(self.note1.id)
        self.assertIsNotNone(self.note1.created_on)
        self.assertIsNotNone(self.note1.updated_at)
        self.assertIsNotNone(self.note2.id)
        self.assertIsNotNone(self.note2.created_on)
        self.assertIsNotNone(self.note2.updated_at)
