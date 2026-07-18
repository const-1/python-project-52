from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Status


class StatusCRUDTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        self.client.login(username="testuser", password="testpass123")

    def test_status_list_view(self):
        response = self.client.get(reverse("statuses:list"))
        self.assertEqual(response.status_code, 200)

    def test_status_create(self):
        response = self.client.post(reverse("statuses:create"), data={"name": "New"})
        self.assertRedirects(response, reverse("statuses:list"))
        self.assertTrue(Status.objects.filter(name="New").exists())

    def test_status_update(self):
        status = Status.objects.create(name="Old")
        response = self.client.post(
            reverse("statuses:update", args=[status.pk]), data={"name": "Updated"}
        )
        self.assertRedirects(response, reverse("statuses:list"))
        status.refresh_from_db()
        self.assertEqual(status.name, "Updated")

    def test_status_delete(self):
        status = Status.objects.create(name="ToDelete")
        response = self.client.post(reverse("statuses:delete", args=[status.pk]))
        self.assertRedirects(response, reverse("statuses:list"))
        self.assertFalse(Status.objects.filter(pk=status.pk).exists())

    def test_login_required(self):
        self.client.logout()
        urls = [reverse("statuses:list"), reverse("statuses:create")]
        for url in urls:
            response = self.client.get(url)
            self.assertRedirects(response, f"{reverse('login')}?next={url}")
