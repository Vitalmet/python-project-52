from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'index.html'


class UsersView(TemplateView):
    template_name = 'users.html'


class LoginView(TemplateView):
    template_name = 'login.html'


class RegisterView(TemplateView):
    template_name = 'register.html'
