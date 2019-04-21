from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.views.decorators.cache import cache_page

from Login.models import UserInfo, Car, ClassList, Pay, Ticket
from global_tools.login_decorate import login
from global_tools.pwd import hashpwd
from Pay.views import aliPay


@login
def person(request):
    user = request.session.get('user')
    ret = {"status": 0, "msg": ""}
    count = Car.objects.filter(user=user).count()
    if request.method == 'GET':
        userinfo = UserInfo.objects.filter(name=user)
        return render(request, 'person/person.html', {"username": user, 'userinfo': userinfo[0], 'count': count})
    pwd = request.POST.get('pwd')
    rpwd = request.POST.get('rpwd')

    # 加密存储

    hash_pwd = hashpwd(pwd)

    exit = UserInfo.objects.filter(name=user, password=hash_pwd)

    if exit:
        # 加密存储

        hash_rpwd = hashpwd(rpwd)
        print(hash_rpwd)
        UserInfo.objects.filter(name=user).update(password=hash_rpwd)
        ret['status'] = 1
        ret['msg'] = "更改成功"
    else:
        ret['msg'] = '密码错误'
    return JsonResponse(ret)


@cache_page(60*1)
@login
def order(request):
    item_list = []  # 创建一个保存商品的列表
    user = request.session.get('user')
    count = Car.objects.filter(user=user).count()
    save_id = request.session.get('recently', '')
    # print('save_id', save_id)
    pay = Pay.objects.filter(p_user=user)
    # print(pay)
    if save_id:
        for id in save_id:
            item = ClassList.objects.filter(l_number=id)
            item_list.append(item[0])

    return render(request, 'person/order.html', {'username': user, 'count': count, 'item_list': item_list, 'pay': pay})


@cache_page(60*1)
@login
def address(request):
    user = request.session.get('user')
    count = Car.objects.filter(user=user).count()
    ret_user = UserInfo.objects.filter(name=user).first()
    # print(ret_user.name)
    return render(request, 'person/address.html', {"user": ret_user, 'username': user, 'count': count})


# 更新收货地址
@login
def address_update(request):
    user = request.POST.get('user')
    receiver = request.POST.get('receiver')
    address = request.POST.get('address')
    code = request.POST.get('code')
    phone = request.POST.get('phone')
    try:
        UserInfo.objects.filter(name=user).update(receiver=receiver, addr=address, code=code, phone=phone)
    except:
        return HttpResponse("没有这个用户！")
    return JsonResponse({"code": 1})


@cache_page(60*1)
@login
def coupon(request):
    ticket_list = Ticket.objects.filter(user__name=request.session.get('user')).values('tName', 'tPrice', 'tDescribe', 'tDate')
    return render(request, 'person/coupon.html', {'ticket': ticket_list, 'username': request.session.get('user')})
