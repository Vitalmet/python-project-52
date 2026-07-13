from django.http import HttpResponse  # ✅ ПРАВИЛЬНО

def index(request):
    return HttpResponse("Welcome to Task Manager!")
