from django.shortcuts import render
from Login.models import *
from django.views.decorators.cache import cache_page
from django.core.cache import cache


def index(request):
    title = AllClass.objects.values('name', 'number').distinct()
    Mylist = []
    for i in title:
        message = AllClass.objects.filter(number=i['number']).values(
            'classlist__name', 'classlist__price', 'classlist__img_url', 'classlist__l_number')[0:5]
        Mylist.append([message, i])
    return render(request, 'index/index.html', {"Mylist": Mylist})

    # phone_list = AllClass.objects.filter(number=10001).values(
    #     'classlist__name', 'classlist__price', 'classlist__img_url')[0:5]
    # home_list = AllClass.objects.filter(number=10002).values(
    #     'classlist__name', 'classlist__price', 'classlist__img_url')[0:5]
    # life_list = AllClass.objects.filter(number=10003).values(
    #     'classlist__name', 'classlist__price', 'classlist__img_url')[0:5]

    # return render(request, 'index/index.html', {"title": title, "phone_list": phone_list, "home_list": home_list, "life_list": life_list})


def list(request):
    name = request.GET.get('id')
    goodsList = AllClass.objects.filter(name=name).values('classlist__name', 'classlist__price', 'classlist__img_url',
                                                          'classlist__l_number')
    return render(request, 'index/list.html', {"goodsList": goodsList, "name": name})



