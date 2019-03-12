from django.shortcuts import render
from Login.models import *


def detail(request):
    id = request.GET.get('id')
    user = request.GET.get('user')
    user = request.session.get(user)
    if user:
        count = UserInfo.objects.filter(name=user).values('car')
        if count:
            count = count[0]['car']
    else:
        user = ''
        count = ''

    detail_list = ClassList.objects.filter(l_number=id).values('l_number', 'name', 'img_url', 'color', 'price',
                                                               'comment__content', 'comment__userinfo__nickname')

    return render(request, 'index/detail.html', {'detail_list': detail_list[0], 'username': user, "count": count})