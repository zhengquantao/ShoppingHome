from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.core.cache import cache


def index(request):
    return render(request, 'index/index.html')