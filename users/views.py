# users/views.py
from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.utils.translation import gettext_lazy as _

from .forms import UserRegisterForm, UserProfileForm
from tasks.models import Task


class UserListView(ListView):
    """Список всех пользователей (доступен без авторизации)"""
    model = User
    template_name = 'users/user_list.html'
    context_object_name = 'users'
    ordering = ['date_joined']


class UserCreateView(CreateView):
    """Регистрация нового пользователя"""
    form_class = UserRegisterForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('login')
    extra_context = {
        'title': _('Registration'),
        'button_text': _('Register'),
    }

    def form_valid(self, form):
        messages.success(self.request, _('User successfully registered'))
        return super().form_valid(form)


class CustomLoginView(LoginView):
    """Вход в систему"""
    template_name = 'users/login.html'
    next_page = reverse_lazy('index')
    extra_context = {
        'title': _('Login'),
        'button_text': _('Log in'),
    }

    def form_valid(self, form):
        messages.success(self.request, _('You are logged in'))
        return super().form_valid(form)


class CustomLogoutView(LogoutView):
    """Выход из системы (только POST)"""
    next_page = reverse_lazy('index')

    def dispatch(self, request, *args, **kwargs):
        messages.success(request, _('You are logged out'))
        return super().dispatch(request, *args, **kwargs)


class UserUpdateView(UserPassesTestMixin, UpdateView):
    """Редактирование профиля пользователя (только для самого пользователя)"""
    model = User
    form_class = UserProfileForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('users_list')
    extra_context = {
        'title': _('Edit user'),
        'button_text': _('Update'),
    }

    def test_func(self):
        return self.get_object() == self.request.user

    def form_valid(self, form):
        messages.success(self.request, _('User successfully updated'))
        return super().form_valid(form)


class UserDeleteView(UserPassesTestMixin, DeleteView):
    """Удаление пользователя (только для самого пользователя)"""
    model = User
    template_name = 'users/user_confirm_delete.html'
    success_url = reverse_lazy('users_list')

    def test_func(self):
        return self.get_object() == self.request.user

    def post(self, request, *args, **kwargs):
        user = self.get_object()
        # Проверяем, есть ли у пользователя задачи, где он автор
        if Task.objects.filter(author=user).exists():
            messages.error(
                request,
                _('Cannot delete user because they are the author of tasks')
            )
            return redirect('users_list')
        messages.success(request, _('User successfully deleted'))
        return super().post(request, *args, **kwargs)
