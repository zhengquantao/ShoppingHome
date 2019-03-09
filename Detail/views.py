from django.shortcuts import render
from Login.models import *


def detail(request):
    id = request.GET.get('id')
    detail_list = ClassList.objects.filter(l_number=id).values('name', 'img_url', 'color', 'price', 'comment__content')
    return render(request, 'index/detail.html', {'detail_list': detail_list[0]})