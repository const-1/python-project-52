# tasks/filters.py
import django_filters
from django import forms
from django.contrib.auth.models import User
from .models import Task
from statuses.models import Status
from tasks.models import Label


class TaskFilter(django_filters.FilterSet):
    """
    Фильтр для задач: по статусу, исполнителю, метке и чекбоксу "Только свои".
    """

    status = django_filters.ModelChoiceFilter(
        queryset=Status.objects.all(), empty_label="---------", label="Статус"
    )
    executor = django_filters.ModelChoiceFilter(
        queryset=User.objects.all(), empty_label="---------", label="Исполнитель"
    )
    labels = django_filters.ModelChoiceFilter(
        queryset=Label.objects.all(), empty_label="---------", label="Метка"
    )
    self_tasks = django_filters.BooleanFilter(
        method="filter_self_tasks",
        widget=forms.CheckboxInput,
        label="Только свои задачи",
    )

    class Meta:
        model = Task
        fields = ["status", "executor", "labels"]

    def filter_self_tasks(self, queryset, name, value):
        """
        Если чекбокс отмечен (value=True), фильтруем задачи,
        где автор — текущий пользователь.
        """
        if value and self.request:
            return queryset.filter(author=self.request.user)
        return queryset
