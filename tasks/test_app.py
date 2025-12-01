from django.test import TestCase, Client
from django.urls import reverse
from datetime import date, timedelta
from tasks.models import Task


class TaskModelTest(TestCase):
    def setUp(self):
        self.task = Task.objects.create(
            title="Test Task",
            description="Test description",
            due_date=date.today() + timedelta(days=5),
            priority="medium",
            completed=False
        )

    def test_task_creation(self):
        self.assertEqual(self.task.title, "Test Task")
        self.assertEqual(str(self.task), "Test Task")
        self.assertFalse(self.task.completed)


class TaskViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.task = Task.objects.create(
            title="View Test Task",
            description="View description",
            due_date=date.today() + timedelta(days=3),
            priority="high",
            completed=False
        )

    def test_task_list_view(self):
        response = self.client.get(reverse('task_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.task.title)
        self.assertTemplateUsed(response, 'tasks/task_list.html')

    def test_add_task_view(self):
        response = self.client.post(reverse('add_task'), {
            'title': 'New Task',
            'description': 'New description',
            'due_date': (date.today() + timedelta(days=2)).isoformat(),
            'priority': 'low'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Task.objects.filter(title='New Task').exists())

    def test_edit_task_view(self):
        response = self.client.post(reverse('edit_task', args=[self.task.id]), {
            'title': 'Updated Task',
            'description': 'Updated description',
            'due_date': (date.today() + timedelta(days=4)).isoformat(),
            'priority': 'medium',
            'completed': 'on'
        })
        self.assertEqual(response.status_code, 302)

        updated = Task.objects.get(id=self.task.id)
        self.assertEqual(updated.title, "Updated Task")
        self.assertEqual(updated.description, "Updated description")
        self.assertTrue(updated.completed)

    def test_delete_task_view(self):
        response = self.client.get(reverse('delete_task', args=[self.task.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Task.objects.filter(id=self.task.id).exists())

    def test_toggle_complete_view(self):
        response = self.client.get(reverse('toggle_complete', args=[self.task.id]))
        self.assertEqual(response.status_code, 302)

        toggled = Task.objects.get(id=self.task.id)
        self.assertTrue(toggled.completed)
