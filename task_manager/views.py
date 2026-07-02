from django.shortcuts import render

def index(request):
    # raise Exception("Test error for Rollbar")  # Временная строка для проверки Rollbar
    return render(request, 'task_manager/index.html')
