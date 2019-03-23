from django.shortcuts import render, redirect, HttpResponseRedirect
from django.http import JsonResponse
from .models import UserInfo
import hashlib


def login(request):
    if request.method == "GET":
        user = request.COOKIES.get('user', '')
        return render(request, 'login/login.html', {'user': user})

    user = request.POST.get('user')
    pwd = request.POST.get('pwd')
    check = request.POST.get('check', 0)  # 记住密码部分没有做

    # 加密存储
    hashs = hashlib.md5(b'123')  # 加密方法
    hashs.update(bytes(pwd, encoding='utf-8'))
    hash_pwd = hashs.hexdigest()

    count = UserInfo.objects.filter(name=user, password=hash_pwd).count()
    if count:
        request.session['user'] = user  #
    # 是否记住密码
    if check:
        request.COOKIES['user'] = user
    else:
        request.COOKIES.clear()

    return JsonResponse({"code": count, 'user': user})


def register(request):
    if request.method == 'GET':
        return render(request, 'login/register.html')
    # POST请求
    user = request.POST.get('user')
    pwd = request.POST.get('pwd')
    email = request.POST.get('email')

    """这里加邮箱验证的"""

    # 加密存储
    hashs = hashlib.md5(b'123')  # 加密方法
    hashs.update(bytes(pwd, encoding='utf-8'))
    hash_pwd = hashs.hexdigest()

    # 创建到数据库
    UserInfo.objects.create(name=user, password=hash_pwd, email=email)
    return JsonResponse({'code': 1})


# 在注册页面检验用户名是否存在
def register_exit(request):
    user = request.GET.get('user')
    count = UserInfo.objects.filter(name=user).count()
    return JsonResponse({'count': count})


def logout(request):
    path = request.path
    print(path)
    # user = request.GET.get('user')  #
    print("这个用户", request.session.get('user'))
    user = request.session.get('user')
    if user:
        ret = request.session.pop('user')  # user
        print(ret)
        return redirect('/login/')
    return redirect('/')

