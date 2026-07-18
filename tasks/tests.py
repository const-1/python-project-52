from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages

from statuses.models import Status
from tasks.models import Task, Label


class TaskCRUDTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="user1", password="pass1")
        self.user2 = User.objects.create_user(username="user2", password="pass2")
        self.status = Status.objects.create(name="New")
        self.label = Label.objects.create(name="Urgent")
        self.client.login(username="user1", password="pass1")

    def test_create_task_author_auto(self):
        response = self.client.post(
            reverse("tasks:create"),
            data={
                "name": "Test Task",
                "description": "Description",
                "status": self.status.id,
                "executor": self.user2.id,
                "labels": [self.label.id],
            },
        )
        self.assertRedirects(response, reverse("tasks:list"))
        task = Task.objects.get(name="Test Task")
        self.assertEqual(task.author, self.user1)
        self.assertEqual(task.status, self.status)
        self.assertEqual(task.executor, self.user2)
        self.assertIn(self.label, task.labels.all())
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Задача успешно создана")

    def test_update_task(self):
        task = Task.objects.create(
            name="Old Name",
            description="Old desc",
            status=self.status,
            author=self.user1,
        )
        response = self.client.post(
            reverse("tasks:update", args=[task.pk]),
            data={
                "name": "Updated Name",
                "description": "Updated desc",
                "status": self.status.id,
                "executor": self.user2.id,
            },
        )
        self.assertRedirects(response, reverse("tasks:list"))
        task.refresh_from_db()
        self.assertEqual(task.name, "Updated Name")
        self.assertEqual(task.description, "Updated desc")
        self.assertEqual(task.executor, self.user2)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Задача успешно изменена")

    def test_delete_task_author_only(self):
        task = Task.objects.create(
            name="ToDelete",
            status=self.status,
            author=self.user1,
        )
        # Попытка удалить от имени user2 (не автор)
        self.client.logout()
        self.client.login(username="user2", password="pass2")
        response = self.client.post(reverse("tasks:delete", args=[task.pk]))
        self.assertRedirects(response, reverse("tasks:list"))
        self.assertTrue(Task.objects.filter(pk=task.pk).exists())
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Задачу может удалить только её автор")
        # Удаление автором
        self.client.logout()
        self.client.login(username="user1", password="pass1")
        response = self.client.post(reverse("tasks:delete", args=[task.pk]))
        self.assertRedirects(response, reverse("tasks:list"))
        self.assertFalse(Task.objects.filter(pk=task.pk).exists())
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Задача успешно удалена")

    def test_list_view_login_required(self):
        self.client.logout()
        urls = [
            reverse("tasks:list"),
            reverse("tasks:create"),
        ]
        for url in urls:
            response = self.client.get(url)
            self.assertRedirects(response, f"{reverse('login')}?next={url}")

    def test_detail_view(self):
        task = Task.objects.create(
            name="Detail Task",
            status=self.status,
            author=self.user1,
        )
        response = self.client.get(reverse("tasks:detail", args=[task.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Detail Task")
        self.assertContains(response, self.status.name)
        self.assertContains(response, self.user1.username)


class TaskFilterTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="user1", password="pass1")
        self.user2 = User.objects.create_user(username="user2", password="pass2")
        self.status1 = Status.objects.create(name="New")
        self.status2 = Status.objects.create(name="In Progress")
        self.label1 = Label.objects.create(name="Urgent")
        self.label2 = Label.objects.create(name="Backlog")

        self.task1 = Task.objects.create(
            name="Task 1", status=self.status1, author=self.user1, executor=self.user2
        )
        self.task1.labels.add(self.label1)

        self.task2 = Task.objects.create(
            name="Task 2", status=self.status2, author=self.user2, executor=self.user1
        )
        self.task2.labels.add(self.label2)

        self.client.login(username="user1", password="pass1")

    def test_filter_by_status(self):
        response = self.client.get(reverse("tasks:list"), {"status": self.status1.id})
        self.assertContains(response, "Task 1")
        self.assertNotContains(response, "Task 2")

    def test_filter_by_executor(self):
        response = self.client.get(reverse("tasks:list"), {"executor": self.user2.id})
        self.assertContains(response, "Task 1")
        self.assertNotContains(response, "Task 2")

    def test_filter_by_label(self):
        response = self.client.get(reverse("tasks:list"), {"labels": self.label1.id})
        self.assertContains(response, "Task 1")
        self.assertNotContains(response, "Task 2")

    def test_filter_self_tasks(self):
        response = self.client.get(reverse("tasks:list"), {"self_tasks": "on"})
        self.assertContains(response, "Task 1")
        self.assertNotContains(response, "Task 2")

    def test_combined_filters(self):
        response = self.client.get(
            reverse("tasks:list"),
            {"status": self.status1.id, "executor": self.user2.id, "self_tasks": "on"},
        )
        self.assertContains(response, "Task 1")
        self.assertNotContains(response, "Task 2")
