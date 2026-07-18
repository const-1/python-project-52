from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages


class UserRegistrationTest(TestCase):
    """Тесты для регистрации пользователя (Create)"""

    def test_registration_success(self):
        """Проверка успешной регистрации"""
        response = self.client.post(
            reverse("user_create"),
            data={
                "username": "testuser",
                "first_name": "Test",
                "last_name": "User",
                "password1": "complexpass123",
                "password2": "complexpass123",
            },
        )
        # Проверка редиректа на страницу входа
        self.assertRedirects(response, reverse("login"))
        # Проверка создания пользователя
        self.assertTrue(User.objects.filter(username="testuser").exists())
        # Проверка flash-сообщения
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Пользователь успешно зарегистрирован")

    def test_registration_with_existing_username(self):
        User.objects.create_user(username="existing", password="pass")
        response = self.client.post(
            reverse("user_create"),
            data={
                "username": "existing",
                "first_name": "Test",
                "last_name": "User",
                "password1": "complexpass123",
                "password2": "complexpass123",
            },
        )
        self.assertEqual(response.status_code, 200)
        # Проверяем, что форма в контексте содержит ошибку для поля username
        form = response.context["form"]
        self.assertIn("username", form.errors)
        self.assertIn("Пользователь с таким именем уже существует.", str(form.errors))
        self.assertEqual(User.objects.filter(username="existing").count(), 1)


class UserLoginTest(TestCase):
    """Тесты для входа в систему"""

    def setUp(self):
        # Создаём пользователя для тестов
        self.user = User.objects.create_user(
            username="testuser", password="complexpass123"
        )

    def test_login_success(self):
        """Успешный вход"""
        response = self.client.post(
            reverse("login"),
            data={
                "username": "testuser",
                "password": "complexpass123",
            },
        )
        self.assertRedirects(response, reverse("index"))
        self.assertTrue(response.wsgi_request.user.is_authenticated)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Вы залогинены")

    def test_login_failure(self):
        """Неправильный пароль"""
        response = self.client.post(
            reverse("login"),
            data={
                "username": "testuser",
                "password": "wrongpassword",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)


class UserUpdateTest(TestCase):
    """Тесты для обновления профиля (Update)"""

    def setUp(self):
        # Создаём двух пользователей: один будет авторизован, другой — чужой
        self.user1 = User.objects.create_user(
            username="user1", password="pass1", first_name="First", last_name="Last"
        )
        self.user2 = User.objects.create_user(
            username="user2", password="pass2", first_name="Other", last_name="User"
        )

    def test_update_own_profile(self):
        """Пользователь может редактировать свой профиль"""
        self.client.login(username="user1", password="pass1")
        response = self.client.post(
            reverse("user_update", args=[self.user1.pk]),
            data={
                "first_name": "NewFirst",
                "last_name": "NewLast",
                "username": "user1",
            },
        )
        self.assertRedirects(response, reverse("users_list"))
        self.user1.refresh_from_db()
        self.assertEqual(self.user1.first_name, "NewFirst")
        self.assertEqual(self.user1.last_name, "NewLast")

        # Проверка flash-сообщения
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Пользователь успешно изменён")

    def test_cannot_update_other_profile(self):
        """Пользователь не может редактировать чужой профиль"""
        self.client.login(username="user1", password="pass1")
        response = self.client.post(
            reverse("user_update", args=[self.user2.pk]),
            data={"first_name": "Hacked", "last_name": "Hacker", "username": "user2"},
        )
        self.assertEqual(response.status_code, 403)


class UserDeleteTest(TestCase):
    """Тесты для удаления пользователя (Delete)"""

    def setUp(self):
        self.user1 = User.objects.create_user(username="user1", password="pass1")
        self.user2 = User.objects.create_user(username="user2", password="pass2")

    # def test_delete_own_profile(self):
    #    self.client.login(username='user1', password='pass1')
    # Отправляем POST-запрос на удаление (без follow)
    #    response = self.client.post(reverse('user_delete', args=[self.user1.pk]))
    # Проверяем редирект
    #    self.assertRedirects(response, reverse('users_list'))
    # Теперь явно запрашиваем страницу списка пользователей
    #    response = self.client.get(reverse('users_list'))
    # Проверяем flash-сообщение на этой странице
    #    messages = list(get_messages(response.wsgi_request))
    #    self.assertEqual(len(messages), 1)
    #    self.assertEqual(str(messages[0]), 'Пользователь успешно удалён')
    # Убеждаемся, что пользователь удалён из БД
    #    self.assertFalse(User.objects.filter(pk=self.user1.pk).exists())

    def test_cannot_delete_other_profile(self):
        """Пользователь не может удалить чужой профиль"""
        self.client.login(username="user1", password="pass1")
        response = self.client.post(reverse("user_delete", args=[self.user2.pk]))
        self.assertEqual(response.status_code, 403)
        self.assertTrue(User.objects.filter(pk=self.user2.pk).exists())


class UserLogoutTest(TestCase):
    """Тесты для выхода из системы"""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="complexpass123"
        )

    def test_logout(self):
        """Проверка выхода из системы"""
        self.client.login(username="testuser", password="complexpass123")
        response = self.client.post(reverse("logout"))
        self.assertRedirects(response, reverse("index"))
        self.assertFalse(response.wsgi_request.user.is_authenticated)

        # Проверка flash-сообщения
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Вы разлогинены")
