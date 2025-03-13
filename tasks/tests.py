from django.test import TestCase
from django.contrib.auth.models import User
from .models import Task


class TaskTestCase(TestCase):
    def setUp(self):
        """Set up a test user and a test task."""
        self.user = User.objects.create(username="testuser")
        self.task = Task.objects.create(
            title="Test Task",
            user=self.user,
            status="new",
            priority="medium",
            deadline=None
        )

    def test_task_creation(self):
        """Test that a task is created correctly."""
        self.assertEqual(self.task.title, "Test Task")
        self.assertEqual(self.task.status, "new")
        self.assertEqual(self.task.priority, "medium")
        self.assertIsNone(self.task.deadline)
        self.assertTrue(self.task.user, "Task should be linked to a user")

    def test_task_string_representation(self):
        """Test the string representation of a task."""
        self.assertEqual(str(self.task), "Test Task")


class UserTestCase(TestCase):
    def test_user_creation(self):
        """Test user creation."""
        user = User.objects.create(username="newuser",
                                   email="newuser@example.com"
                                   )
        self.assertEqual(user.username, "newuser")
        self.assertEqual(user.email, "newuser@example.com")
