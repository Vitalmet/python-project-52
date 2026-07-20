from django.contrib import admin
from django.urls import path
from task_manager import views
from django.contrib.auth.views import CustomLogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.IndexView.as_view(), name='index'),

    # Пользователи
    path('users/', views.UsersView.as_view(), name='users'),
    path('users/create/', views.UserCreateView.as_view(), name='user_create'),
    path('users/<int:pk>/update/', views.UserUpdateView.as_view(), name='user_update'),
    path('users/<int:pk>/delete/', views.UserDeleteView.as_view(), name='user_delete'),

    # Аутентификация
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),

    # Статусы
    path('statuses/', views.StatusesView.as_view(), name='statuses'),
    path('statuses/create/', views.StatusCreateView.as_view(), name='status_create'),
    path('statuses/<int:pk>/update/', views.StatusUpdateView.as_view(), name='status_update'),
    path('statuses/<int:pk>/delete/', views.StatusDeleteView.as_view(), name='status_delete'),

    # Задачи
    path('tasks/', views.TasksView.as_view(), name='tasks'),
    path('tasks/create/', views.TaskCreateView.as_view(), name='task_create'),
    path('tasks/<int:pk>/', views.TaskDetailView.as_view(), name='task_detail'),
    path('tasks/<int:pk>/update/', views.TaskUpdateView.as_view(), name='task_update'),
    path('tasks/<int:pk>/delete/', views.TaskDeleteView.as_view(), name='task_delete'),

    # Метки
    path('labels/', views.LabelsView.as_view(), name='labels'),
    path('labels/create/', views.LabelCreateView.as_view(), name='label_create'),
    path('labels/<int:pk>/update/', views.LabelUpdateView.as_view(), name='label_update'),
    path('labels/<int:pk>/delete/', views.LabelDeleteView.as_view(), name='label_delete'),
]
