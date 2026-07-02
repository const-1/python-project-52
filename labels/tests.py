from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from tasks.models import Label, Task, Status

class LabelCRUDTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='pass')
        self.client.login(username='test', password='pass')

    def test_create_label(self):
        response = self.client.post(reverse('labels:create'), {'name': 'Urgent'})
        self.assertRedirects(response, reverse('labels:list'))
        self.assertTrue(Label.objects.filter(name='Urgent').exists())

    def test_update_label(self):
        label = Label.objects.create(name='Old')
        response = self.client.post(reverse('labels:update', args=[label.pk]), {'name': 'New'})
        self.assertRedirects(response, reverse('labels:list'))
        label.refresh_from_db()
        self.assertEqual(label.name, 'New')

    def test_delete_label_with_task(self):
        label = Label.objects.create(name='DeleteMe')
        status = Status.objects.create(name='New')
        task = Task.objects.create(name='Test', status=status, author=self.user)
        task.labels.add(label)
        response = self.client.post(reverse('labels:delete', args=[label.pk]))
        self.assertRedirects(response, reverse('labels:list'))
        self.assertTrue(Label.objects.filter(pk=label.pk).exists())

    def test_delete_label_without_task(self):
        label = Label.objects.create(name='DeleteMe')
        response = self.client.post(reverse('labels:delete', args=[label.pk]))
        self.assertRedirects(response, reverse('labels:list'))
        self.assertFalse(Label.objects.filter(pk=label.pk).exists())

    def test_login_required(self):
        self.client.logout()
        urls = [reverse('labels:list'), reverse('labels:create')]
        for url in urls:
            response = self.client.get(url)
            self.assertRedirects(response, f'{reverse("login")}?next={url}')
