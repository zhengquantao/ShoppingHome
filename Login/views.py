from django.shortcuts import render, redirect, HttpResponseRedirect
from django.http import JsonResponse
from .models import UserInfo
from global_tools.pwd import hashpwd


def login(request):
    if request.method == "GET":
        user = request.COOKIES.get('user', '')
        pwd = request.COOKIES.get('pwd', '')
        return render(request, 'login/login.html', {'user': user, 'pwd': pwd})

    user = request.POST.get('user')
    pwd = request.POST.get('pwd')
    check = request.POST.get('check', 0)  # 记住密码部分没有做

    # 加密存储
    hash_pwd = hashpwd(pwd)

    count = UserInfo.objects.filter(name=user, password=hash_pwd).count()

    # 是否记住密码
    if check:
        request.COOKIES['user'] = user
        request.COOKIES['pwd'] = pwd
    else:
        request.COOKIES.clear()

    if count:
        request.session['user'] = user  # 个人信息存入session
        red = request.COOKIES.get('url', '')  # 是否是从其他页面进来的
        if red:
            return JsonResponse({"code": count, 'user': user, 'path': red})

    return JsonResponse({"code": count, 'user': user, 'path': '/'})


def register(request):
    if request.method == 'GET':
        return render(request, 'login/register.html')
    # POST请求
    user = request.POST.get('user')
    pwd = request.POST.get('pwd')
    email = request.POST.get('email')

    """这里加邮箱验证的"""

    # 加密存储

    hash_pwd = hashpwd(pwd)

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
        request.session.pop('user')  # 删除user
        request.COOKIES.pop('url')
        # request.COOKIES.pop('pwd')
        return redirect('/login/')
    return redirect('/')

