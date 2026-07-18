from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from django.contrib import messages
from django.shortcuts import redirect
from .models import Task
from .forms import TaskForm
from .filters import TaskFilter
from django_filters.views import FilterView


class TaskListView(LoginRequiredMixin, FilterView):
    model = Task
    template_name = "tasks/index.html"
    context_object_name = "tasks"
    filterset_class = TaskFilter

    def get_queryset(self):
        return Task.objects.all()


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/form.html"
    success_url = reverse_lazy("tasks:list")
    extra_context = {"title": "Создать задачу", "button_text": "Создать"}

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, "Задача успешно создана")
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/form.html"
    success_url = reverse_lazy("tasks:list")
    extra_context = {"title": "Изменить задачу", "button_text": "Изменить"}

    def form_valid(self, form):
        messages.success(self.request, "Задача успешно изменена")
        return super().form_valid(form)


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = "tasks/confirm_delete.html"
    success_url = reverse_lazy("tasks:list")
    extra_context = {"title": "Удалить задачу", "button_text": "Да, удалить"}

    def dispatch(self, request, *args, **kwargs):
        task = self.get_object()
        if task.author != request.user:
            messages.error(request, "Задачу может удалить только её автор")
            return redirect("tasks:list")
        return super().dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Задача успешно удалена")
        return super().delete(request, *args, **kwargs)


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = "tasks/detail.html"
    context_object_name = "task"
