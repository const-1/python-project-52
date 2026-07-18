from django import forms
from django.contrib.auth.models import User
from .models import Task, Label


class UserChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.get_full_name() or obj.username


class TaskForm(forms.ModelForm):
    labels = forms.ModelMultipleChoiceField(
        queryset=Label.objects.all(),
        widget=forms.SelectMultiple,
        required=False,
        label="Метки",
    )
    executor = UserChoiceField(
        queryset=User.objects.all(),
        required=False,
        label="Исполнитель",
    )

    class Meta:
        model = Task
        fields = ["name", "description", "status", "executor", "labels"]
        labels = {
            "name": "Имя",
            "description": "Описание",
            "status": "Статус",
            "executor": "Исполнитель",
        }
