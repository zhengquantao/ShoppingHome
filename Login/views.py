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
    # 请求得到access_token
    redirect_uri = "http://127.0.0.1:8000/login/weibo/"
    get_Access_token_url = "https://api.weibo.com/oauth2/access_token?client_id={}&client_secret={}&redirect_uri={}&code={}".format(
        client_id, client_secret, redirect_uri, code)
    response = requests.post(url=get_Access_token_url).text
    response_loads = json.loads(response)
    print(response_loads)
    access_token = response_loads['access_token']
    print(access_token)
    uid = response_loads['uid']
    # 请求得到用户信息
    get_message_url = "https://api.weibo.com/2/users/show.json?access_token={}&uid={}&redirect_uri={}".format(
        access_token, uid, redirect_uri)
    info_message = requests.get(url=get_message_url).text
    info_message_loads = json.loads(info_message)
    user = info_message_loads['name']
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


def proxy_qq(request):
    code = request.GET.get('code')
    client_id, client_secret = qq()
    # 请求得到access_token
    redirect_uri = "http://127.0.0.1:8000/login/qq"
    get_Access_token_url = "https://graph.qq.com/oauth2.0/token?grant_type=authorization_code&client_id={}&client_secret={}&redirect_uri={}&code={}".format(
        client_id, client_secret, redirect_uri, code)
    response = requests.get(url=get_Access_token_url).text
    # print(response)
    # FFFB91C30F6F87EA5BF9570AEC2E23F & expires_in = 7776000 & refresh_token = 7
    # F135B51779C7595DED58D85C87419CE
    # print(access_token)
    access_token = response.split('&')[0]
    access_token = access_token[13:]

    # 获取openid
    get_open_id_url = "https://graph.qq.com/oauth2.0/me?access_token={}".format(access_token)
    response_open_id = requests.get(url=get_open_id_url).text
    # print(response_open_id)
    # callback({"client_id": "101576925", "openid": "B3F2C9D7A081D39936017FF97166052A"});
    response_open_id_dict = eval(response_open_id[9:-3])
    open_id = response_open_id_dict.get('openid')
    # 获取个人信息
    get_user_info_url = "https://graph.qq.com/user/get_user_info?access_token={}&oauth_consumer_key={}&openid={}".format(
        access_token, client_id, open_id
    )

    response_user_info = requests.get(url=get_user_info_url).text
    response_user_info = json.loads(response_user_info)
    user = response_user_info['nickname']

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
    # 请求得到access_token
    redirect_uri = "http://127.0.0.1:8000/login/weixin/"
    get_Access_token_url = "https://api.weixin.qq.com/sns/oauth2/access_token?appid={}&secret={}&code={}&grant_type=authorization_code".format(
        client_id, client_secret, code)
    response = requests.get(url=get_Access_token_url).text
    # print(response)
    # FFFB91C30F6F87EA5BF9570AEC2E23F & expires_in = 7776000 & refresh_token = 7
    # F135B51779C7595DED58D85C87419CE
    # print(access_token)
    access_token = response.split('&')[0]
    access_token = access_token[13:]

    # 获取openid
    get_open_id_url = "".format(
        access_token)
    response_open_id = requests.get(url=get_open_id_url).text
    # print(response_open_id)
    # callback({"client_id": "101576925", "openid": "B3F2C9D7A081D39936017FF97166052A"});
    response_open_id_dict = eval(response_open_id[9:-3])
    open_id = response_open_id_dict.get('openid')
    # 获取个人信息
    get_user_info_url = "https://graph.qq.com/user/get_user_info?access_token={}&oauth_consumer_key={}&openid={}".format(
        access_token, client_id, open_id
    )

    response_user_info = requests.get(url=get_user_info_url).text
    response_user_info = json.loads(response_user_info)
    user = response_user_info['nickname']

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