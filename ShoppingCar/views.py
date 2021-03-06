from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.cache import cache_page

from Login.models import *
from global_tools.login_decorate import login


# 购物车增加数据
@cache_page(60*1)
@login
def shopping_car(request):
    user = request.session.get('user')
    lid = request.GET.get('id')
    count = request.GET.get('count', 1)
    if not user or not lid:
        return JsonResponse({"code": "没有这个用户名！"})
    # class_list = ClassList.objects.filter(l_number=lid)[0]
    # print(class_list.l_number)
    # 获取UserInfo的object
    name = UserInfo.objects.get(name=user)
    id = ClassList.objects.get(l_number=lid)
    Car.objects.create(user=name, count=int(count), class_item=id)
    count = Car.objects.filter(user=user).count()  # 找到登入人的信息
    # print("userinfo", count)
    # userinfo.update(count=count)
    # count = userinfo.values('car')
    # print(count)
    return JsonResponse({"code": 1, "count": count})


# 查看购物车
@cache_page(60*1)
@login
def car_show(request):
    # user = request.GET.get('user') #
    # id = request.GET.get('id')
    user = request.session.get('user')
    if user:
        count = Car.objects.filter(user=user).count()
        if count:
            count = count
    else:
        user = ''
        count = ''
    item_list = Car.objects.filter(user=user).values('id', 'class_item__l_number', 'class_item__img_url', 'class_item__name', 'class_item__price', 'count')

    return render(request, 'index/shoppingcar.html', {"list": item_list, 'count': count, 'username': user})


# 删除信息
@cache_page(60*1)
def car_update(request):
    cid = request.GET.get('id')
    user = request.session.get('user')

    try:
        Car.objects.filter(id=cid).delete()
        if user:
            count = Car.objects.filter(user=user).count()
        else:
            count = ''
        code = 1
    except:
        code = 0
        count = ''
    return JsonResponse({'code': code, 'count': count})
