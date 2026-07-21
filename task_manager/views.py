from django.shortcuts import redirect
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout
from django.contrib.messages.views import SuccessMessageMixin
from .models import Status, Task, Label
from django_filters.views import FilterView
from .filters import TaskFilter
from .forms import (
    CustomUserCreationForm,
    CustomUserChangeForm,
    StatusForm,
    TaskForm,
    LabelForm
)


class IndexView(TemplateView):
    template_name = 'index.html'


class UsersView(ListView):
    model = User
    template_name = 'users.html'
    context_object_name = 'users'
    ordering = ['id']


class UserCreateView(SuccessMessageMixin, CreateView):
    form_class = CustomUserCreationForm
    template_name = 'user_create.html'
    success_url = reverse_lazy('login')
    success_message = 'Пользователь успешно зарегистрирован'

    def form_valid(self, form):
        print("Form is valid, redirecting to login")
        return super().form_valid(form)

    def form_invalid(self, form):
        print("Form is invalid:", form.errors)
        return super().form_invalid(form)


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

class CustomLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        messages.success(request, 'Вы разлогинены')
        return super().dispatch(request, *args, **kwargs)


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



# ========== CRUD для задач ==========

class TaskCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'task_create.html'
    success_url = reverse_lazy('tasks')
    success_message = 'Задача успешно создана'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'task_update.html'
    success_url = reverse_lazy('tasks')
    success_message = 'Задача успешно изменена'


class TaskDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Task
    template_name = 'task_delete.html'
    success_url = reverse_lazy('tasks')
    success_message = 'Задача успешно удалена'

    def dispatch(self, request, *args, **kwargs):
        task = self.get_object()
        if request.user != task.author:
            messages.error(request, 'Задачу может удалить только ее автор')
            return redirect('tasks')
        return super().dispatch(request, *args, **kwargs)


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'task_detail.html'
    context_object_name = 'task'


# ========== CRUD для меток ==========

class LabelsView(LoginRequiredMixin, ListView):
    model = Label
    template_name = 'labels.html'
    context_object_name = 'labels'
    ordering = ['id']


class LabelCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Label
    form_class = LabelForm
    template_name = 'label_create.html'
    success_url = reverse_lazy('labels')
    success_message = 'Метка успешно создана'


class LabelUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Label
    form_class = LabelForm
    template_name = 'label_update.html'
    success_url = reverse_lazy('labels')
    success_message = 'Метка успешно изменена'


class LabelDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Label
    template_name = 'label_delete.html'
    success_url = reverse_lazy('labels')
    success_message = 'Метка успешно удалена'

    def post(self, request, *args, **kwargs):
        label = self.get_object()
        if label.tasks.exists():
            messages.error(request, 'Невозможно удалить метку')
            return redirect('labels')
        return super().post(request, *args, **kwargs)


# ========== CRUD для фильтрации ==========

class TasksView(LoginRequiredMixin, FilterView):
    model = Task
    template_name = 'tasks.html'
    context_object_name = 'tasks'
    filterset_class = TaskFilter
    ordering = ['id']
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        # Применяем фильтр
        self.filterset = self.filterset_class(
            self.request.GET,
            queryset=queryset,
            request=self.request
        )
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filterset
        return context
