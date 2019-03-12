from django.shortcuts import render
from django.http import JsonResponse
from Login.models import *


# 购物车增加数据
def shopping_car(request):
    user = request.GET.get('user')
    lid = request.GET.get('id')
    if not user or not lid:
        return JsonResponse({"code": "没有这个用户名！"})
    class_list = ClassList.objects.filter(l_number=lid)[0]
    print(class_list.l_number)
    car_obj = Car.objects.create(
        l_number=class_list.l_number, name=class_list.name, color=class_list.color,
        price=class_list.price, count=class_list.count, img_url=class_list.img_url)
    userinfo = UserInfo.objects.filter(name=user)  # 找到登入人的信息
    userinfo.update(car=car_obj)
    count = userinfo.values('car')
    # print(count)
    return JsonResponse({"code": 1, "count": count[0]['car']})


def car_show(request):
    pass
    return render(request, 'index/shoppingcar.html')


def car_update(request):
    pass
