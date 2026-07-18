from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from tasks.models import Label, Task
from .forms import LabelForm


class LabelListView(LoginRequiredMixin, ListView):
    model = Label
    template_name = "labels/index.html"
    context_object_name = "labels"


class LabelCreateView(LoginRequiredMixin, CreateView):
    model = Label
    form_class = LabelForm
    template_name = "labels/form.html"
    success_url = reverse_lazy("labels:list")
    extra_context = {"title": "Создать метку", "button_text": "Создать"}

    def form_valid(self, form):
        messages.success(self.request, "Метка успешно создана")
        return super().form_valid(form)


class LabelUpdateView(LoginRequiredMixin, UpdateView):
    model = Label
    form_class = LabelForm
    template_name = "labels/form.html"
    success_url = reverse_lazy("labels:list")
    extra_context = {"title": "Изменить метку", "button_text": "Изменить"}

    def form_valid(self, form):
        messages.success(self.request, "Метка успешно изменена")
        return super().form_valid(form)


class LabelDeleteView(LoginRequiredMixin, DeleteView):
    model = Label
    template_name = "labels/confirm_delete.html"
    success_url = reverse_lazy("labels:list")
    extra_context = {"title": "Удалить метку", "button_text": "Да, удалить"}

    def post(self, request, *args, **kwargs):
        label = self.get_object()
        if Task.objects.filter(labels=label).exists():
            messages.error(request, "Невозможно удалить метку")
            return redirect("labels:list")
        messages.success(request, "Метка успешно удалена")
        return super().post(request, *args, **kwargs)
