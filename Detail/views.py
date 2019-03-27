from django.shortcuts import render
from Login.models import *

save_id = []  # 创建一个空列表


def detail(request):
    id = request.GET.get('id')
    # user = request.GET.get('user')
    user = request.session.get('user')
    if id not in save_id:   # 去重
        save_id.append(id)
    if len(save_id) > 5:  # 默认最近5条浏览记录
        save_id.pop(0)
    request.session['recently'] = save_id
    # print('====', request.session.get('recently'))
    if user:
        count = Car.objects.filter(user=user).count()
        if count:
            count = count
    else:
        user = ''
        count = ''

    detail_list = ClassList.objects.filter(l_number=id).values('l_number', 'name', 'img_url', 'color', 'price',
                                                               'comment__content', 'comment__userinfo__nickname')

    return render(request, 'index/detail.html', {'detail_list': detail_list[0], 'username': user, "count": count})