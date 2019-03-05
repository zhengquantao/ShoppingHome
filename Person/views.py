from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from Login.models import UserInfo


def person(request):
    return render(request, 'person/person.html')


def order(request):
    return render(request, 'person/order.html')


def address(request):
    user = request.session.get('user')
    ret_user = UserInfo.objects.filter(name=user).first()
    # print(ret_user.name)
    return render(request, 'person/address.html', {"user": ret_user})


# 更新收货地址
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
