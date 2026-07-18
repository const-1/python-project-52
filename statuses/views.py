from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib import messages

from .models import Status
from .forms import StatusForm
from tasks.models import Task


class StatusListView(LoginRequiredMixin, ListView):
    model = Status
    template_name = "statuses/index.html"
    context_object_name = "statuses"


class StatusCreateView(LoginRequiredMixin, CreateView):
    model = Status
    form_class = StatusForm
    template_name = "statuses/form.html"
    success_url = reverse_lazy("statuses:list")
    extra_context = {
        "title": "Создать статус",
        "button_text": "Создать",
    }

    def form_valid(self, form):
        messages.success(self.request, "Статус успешно создан")
        return super().form_valid(form)


class StatusUpdateView(LoginRequiredMixin, UpdateView):
    model = Status
    form_class = StatusForm
    template_name = "statuses/form.html"
    success_url = reverse_lazy("statuses:list")
    extra_context = {
        "title": "Редактирование статуса",
        "button_text": "Изменить",
    }

    def form_valid(self, form):
        messages.success(self.request, "Статус успешно изменен")
        return super().form_valid(form)


class StatusDeleteView(LoginRequiredMixin, DeleteView):
    model = Status
    template_name = "statuses/confirm_delete.html"
    success_url = reverse_lazy("statuses:list")
    extra_context = {
        "title": "Удаление статуса",
        "button_text": "Да, удалить",
    }

    def post(self, request, *args, **kwargs):
        status = self.get_object()
        if Task.objects.filter(status=status).exists():
            messages.error(
                request,
                "Невозможно удалить статус, так как он используется в задачах"
            )
            return redirect("statuses:list")
        messages.success(request, "Статус успешно удален")
        return super().post(request, *args, **kwargs)
