from django.shortcuts import render, HttpResponse


def login(request):
    return render(request, 'login/login.html')


def register(request):
    return render(request, 'login/register.html')
