from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout
from django.contrib.messages.views import SuccessMessageMixin
from django.views import View
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from .models import Status
from .forms import CustomUserCreationForm, CustomUserChangeForm, StatusForm


class IndexView(TemplateView):
    template_name = 'index.html'


class UsersView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'users.html'
    context_object_name = 'users'
    ordering = ['id']


class UserCreateView(SuccessMessageMixin, CreateView):
    form_class = CustomUserCreationForm
    template_name = 'user_create.html'
    success_url = reverse_lazy('login')
    success_message = 'Пользователь успешно зарегистрирован'


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    form_class = CustomUserChangeForm
    template_name = 'user_update.html'
    success_url = reverse_lazy('users')
    success_message = 'Пользователь успешно изменен'

    def dispatch(self, request, *args, **kwargs):
        user = self.get_object()
        if request.user != user:
            messages.error(request, 'У вас нет прав для изменения')
            return redirect('users')
        return super().dispatch(request, *args, **kwargs)


class UserDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = User
    template_name = 'user_delete.html'
    success_url = reverse_lazy('users')
    success_message = 'Пользователь успешно удален'

    def dispatch(self, request, *args, **kwargs):
        user = self.get_object()
        if request.user != user:
            messages.error(request, 'У вас нет прав для изменения')
            return redirect('users')
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        logout(request)
        return super().post(request, *args, **kwargs)


class CustomLoginView(LoginView):
    template_name = 'login.html'
    success_message = 'Вы залогинены'

    def get_success_url(self):
        return reverse_lazy('index')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return response


# ========== CRUD для статусов ==========

class StatusesView(LoginRequiredMixin, ListView):
    model = Status
    template_name = 'statuses.html'
    context_object_name = 'statuses'
    ordering = ['id']


class StatusCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Status
    form_class = StatusForm
    template_name = 'status_create.html'
    success_url = reverse_lazy('statuses')
    success_message = 'Статус успешно создан'


class StatusUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Status
    form_class = StatusForm
    template_name = 'status_update.html'
    success_url = reverse_lazy('statuses')
    success_message = 'Статус успешно изменен'


class StatusDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Status
    template_name = 'status_delete.html'
    success_url = reverse_lazy('statuses')
    success_message = 'Статус успешно удален'

    def post(self, request, *args, **kwargs):
        status = self.get_object()
        # Проверка, есть ли задачи со статусом
        if hasattr(status, 'tasks') and status.tasks.exists():
            messages.error(request, 'Невозможно удалить статус')
            return redirect('statuses')
        return super().post(request, *args, **kwargs)