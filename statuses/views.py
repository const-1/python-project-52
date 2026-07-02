from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.utils.translation import gettext_lazy as _

from .models import Status
from .forms import StatusForm
from tasks.models import Task


class StatusListView(LoginRequiredMixin, ListView):
    model = Status
    template_name = 'statuses/index.html'
    context_object_name = 'statuses'


class StatusCreateView(LoginRequiredMixin, CreateView):
    model = Status
    form_class = StatusForm
    template_name = 'statuses/form.html'
    success_url = reverse_lazy('statuses:list')
    extra_context = {
        'title': _('Create status'),
        'button_text': _('Create'),
    }

    def form_valid(self, form):
        messages.success(self.request, _('Status successfully created'))
        return super().form_valid(form)


class StatusUpdateView(LoginRequiredMixin, UpdateView):
    model = Status
    form_class = StatusForm
    template_name = 'statuses/form.html'
    success_url = reverse_lazy('statuses:list')
    extra_context = {
        'title': _('Edit status'),
        'button_text': _('Update'),
    }

    def form_valid(self, form):
        messages.success(self.request, _('Status successfully updated'))
        return super().form_valid(form)


class StatusDeleteView(LoginRequiredMixin, DeleteView):
    model = Status
    template_name = 'statuses/confirm_delete.html'
    success_url = reverse_lazy('statuses:list')
    extra_context = {
        'title': _('Delete status'),
        'button_text': _('Yes, delete'),
    }

    def post(self, request, *args, **kwargs):
        status = self.get_object()
        if Task.objects.filter(status=status).exists():
            messages.error(request, _('Cannot delete status because it is used in tasks'))
            return redirect('statuses:list')
        messages.success(request, _('Status successfully deleted'))
        return super().post(request, *args, **kwargs)
