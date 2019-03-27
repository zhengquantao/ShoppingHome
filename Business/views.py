from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from global_tools.pwd import hashpwd
from Business.models import Binfo

# Create your views here.


def login(request):
    if request.method == "GET":
        return render(request, 'business/login.html')
    user = request.POST.get('user')
    pwd = request.POST.get('pwd')
    # check = request.POST.get('check', 0)  # 记住密码部分没有做

    # 加密存储
    # hash_pwd = hashpwd(pwd)

    count = Binfo.objects.filter(name=user, password=pwd).count()

    if count:
        request.session['user'] = user  # 个人信息存入session
    #     red = request.COOKIES.get('url', '')  # 是否是从其他页面进来的
    #     if red:
    #         return JsonResponse({"code": count, 'user': user, 'path': red})

    return JsonResponse({"code": count, 'username': user, 'path': '/business/index/'})


def index(request):
    user = request.session.get('user')
    return render(request, 'business/index.html', {'username': user})


def shop(request):
    user = request.session.get('user')
    return render(request, 'business/order.html', {'username': user})


def message(request):
    user = request.session.get('user')
    return render(request, 'business/message.html', {'username': user})


def list(request):
    user = request.session.get('user')
    return render(request, 'business/list.html', {'username': user})


def add(request):
    user = request.session.get('user')
    return render(request, 'business/add.html', {'username': user})


def update(request):
    user = request.session.get('user')
    return render(request, 'business/update.html', {'username': user})


def ad(request):
    user = request.session.get('user')
    return render(request, 'business/ad.html', {'username': user})