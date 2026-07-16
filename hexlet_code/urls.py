from django.contrib import admin
from django.urls import path
from task_manager import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.IndexView.as_view(), name='index'),
    path('users/', views.UsersView.as_view(), name='users'),
    path('users/create/', views.UserCreateView.as_view(), name='user_create'),
    path('users/<int:pk>/update/', views.UserUpdateView.as_view(), name='user_update'),
    path('users/<int:pk>/delete/', views.UserDeleteView.as_view(), name='user_delete'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    # Статусы
    path('statuses/', views.StatusesView.as_view(), name='statuses'),
    path('statuses/create/', views.StatusCreateView.as_view(), name='status_create'),
    path('statuses/<int:pk>/update/', views.StatusUpdateView.as_view(), name='status_update'),
    path('statuses/<int:pk>/delete/', views.StatusDeleteView.as_view(), name='status_delete'),
]
