from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from .models import UserInfo
from global_tools.pwd import hashpwd
from global_tools.image import img
from global_tools.send_email import sender_email
from global_tools.login_key import weibo, qq, weixin, proxy_urls
import requests
import json
import uuid
from AgentLogin import AgentLogin
from django.core.cache import cache


def login(request):
    code_item = ''

    if request.method == "GET":
        user = request.COOKIES.get('user', '')
        pwd = request.COOKIES.get('pwd', '')
        code = img()
        for item in code:
            code_item += str(item)
        # print(code_item)
        request.session['code'] = code_item
        img_path = '/static/images/code.jpg'
        proxy_url = proxy_urls()
        return render(request, 'login/login.html', {'user': user, 'pwd': pwd, 'img_path': img_path, "proxy_url": proxy_url})

    user = request.POST.get('user')
    pwd = request.POST.get('pwd')
    check_code = request.POST.get('check_code')
    for item in request.session.get('code'):
        code_item += str(item)
    # print(user, pwd, check_code, request.session.get('code'))
    if check_code != code_item:
        return JsonResponse({"code": 2, 'user': user})  # 验证码错误

    check = request.POST.get('check', 0)  # 记住密码部分没有做

    # 加密存储
    hash_pwd = hashpwd(pwd)

    if cache.get(user) == hash_pwd:  # 判断跟Redis缓存中是否一致
        if check:
            request.COOKIES['user'] = user
            request.COOKIES['pwd'] = pwd
        else:
            request.COOKIES.clear()

        request.session['user'] = user  # 个人信息存入session
        red = request.COOKIES.get('url', '')  # 是否是从其他页面进来的
        if red:
            try:
                request.session.pop('code')
            except:
                pass
            return JsonResponse({"code": 1, 'user': user, 'path': red})
        try:
            request.session.pop('code')
        except:
            pass
        return JsonResponse({"code": 1, 'user': user, 'path': '/'})

    # Redis中没有
    count = UserInfo.objects.filter(name=user, password=hash_pwd).count()

    # 是否记住密码
    if check:
        request.COOKIES['user'] = user
        request.COOKIES['pwd'] = pwd
    else:
        request.COOKIES.clear()

    if count:
        cache.set(user, pwd)
        request.session['user'] = user  # 个人信息存入session
        red = request.COOKIES.get('url', '')  # 是否是从其他页面进来的
        if red:
            try:
                request.session.pop('code')
            except:
                pass
            return JsonResponse({"code": count, 'user': user, 'path': red})
    try:
        request.session.pop('code')
    except:
        pass
    return JsonResponse({"code": count, 'user': user, 'path': '/'})


def register(request):
    if request.method == 'GET':
        return render(request, 'login/register.html')
    # POST请求
    user = request.POST.get('user')
    pwd = request.POST.get('pwd')
    email = request.POST.get('email')
    # print(pwd)
    check_message = request.POST.get('check_message')

    """这里加邮箱验证的"""
    if check_message != request.session.get('email_code'):
        return JsonResponse({})

    # 加密存储
    hash_pwd = hashpwd(pwd)

    # 删除session里的email
    request.session.pop('email_code')

    # 创建到数据库
    UserInfo.objects.create(name=user, password=hash_pwd, email=email)
    return JsonResponse({'code': 1, 'path': '/login/'})


# 在注册页面检验用户名是否存在
def register_exit(request):
    user = request.GET.get('user')
    count = UserInfo.objects.filter(name=user).count()
    return JsonResponse({'count': count})


# 图片验证
def check_img(request):
    c_img = img()
    request.session['code'] = c_img
    return JsonResponse({})


# 邮箱验证
def email(request):
    receiver = request.GET.get('check_message')
    email_code = sender_email(receiver)
    # print(email_code)
    if email_code:
        request.session['email_code'] = email_code
        return JsonResponse({'status': 1})
    return JsonResponse({})


def logout(request):
    path = request.path
    print(path)
    # user = request.GET.get('user')  #
    print("这个用户", request.session.get('user'))
    user = request.session.get('user')
    if user:
        request.session.pop('user')  # 删除user
        if request.COOKIES.get('url'):
            request.COOKIES.pop('url')
        # request.COOKIES.pop('pwd')
        return redirect('/login/')
    return redirect('/')


def proxy_weibo(request):
    code = request.GET.get('code')
    client_id, client_secret = weibo()
    redirect_uri = "http://127.0.0.1:8000/login/weibo/"
    user = AgentLogin.weibo(client_id, client_secret, redirect_uri, code)
    is_user = UserInfo.objects.filter(name=user)
    if is_user:
        token = str(uuid.uuid4())
        is_user.update(password=token)
    else:
        token = str(uuid.uuid4())
        UserInfo.objects.create(name=user, password=token)

    # 拿到请求路径
    # path = request.get_host()
    # print(is_safe_url("http://127.0.0.1:8080/home", allowed_hosts={"127.0.0.1:8080"}))
    request.session['user'] = user
    redirect_url = redirect("http://127.0.0.1:8000")
    redirect_url.set_cookie("name", user.encode('utf-8').decode('latin-1'))
    redirect_url.set_cookie("token", token)

    return redirect_url


def proxy_qq(request):
    code = request.GET.get('code')
    client_id, client_secret = qq()
    redirect_uri = "http://127.0.0.1:8000/login/qq"
    user = AgentLogin.qq(client_id, client_secret, redirect_uri, code)

    # 存入数据库
    is_user = UserInfo.objects.filter(name=user)
    if is_user:
        token = str(uuid.uuid4())
        is_user.update(password=token)
    else:
        token = str(uuid.uuid4())
        UserInfo.objects.create(name=user, password=token)

    # 拿到请求路径
    # path = request.get_host()
    # print(is_safe_url("http://127.0.0.1:8080/home", allowed_hosts={"127.0.0.1:8080"}))
    request.session['user'] = user
    redirect_url = redirect("http://127.0.0.1:8000")
    redirect_url.set_cookie("name", user.encode('utf-8').decode('latin-1'))
    redirect_url.set_cookie("token", token)

    return redirect_url


def proxy_weixin(request):
    return HttpResponse("error")
    code = request.GET.get('code')
    client_id, client_secret = weixin()
    user = AgentLogin.weixin(client_id, client_secret, code)
    # 存入数据库
    is_user = UserInfo.objects.filter(name=user)
    if is_user:
        token = str(uuid.uuid4())
        is_user.update(password=token)
    else:
        token = str(uuid.uuid4())
        UserInfo.objects.create(name=user, password=token)

    request.session['user'] = user
    redirect_url = redirect("http://127.0.0.1:8000")
    redirect_url.set_cookie("name", user.encode('utf-8').decode('latin-1'))
    redirect_url.set_cookie("token", token)

    return redirect_url