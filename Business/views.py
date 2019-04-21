from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from django.views.decorators.cache import cache_page

from global_tools.pwd import hashpwd
# from Business.models import Binfo
from django.db.models import Count, Sum
from Login.models import AllClass, ClassList, Border, Binfo, Chat
from functools import wraps
# Create your views here.


def decorate(func):
    @wraps(func)
    def inner(request, *args, **kwargs):
        user = request.session.get('user')  #
        user = Binfo.objects.filter(name=user)
        if user:
            return func(request, *args, **kwargs)
        else:
            return redirect('/business/login/')
    return inner


@cache_page(60*1)
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
        request.session['user'] = user  # 个人信息存入session  #
    #     red = request.COOKIES.get('url', '')  # 是否是从其他页面进来的
    #     if red:
    #         return JsonResponse({"code": count, 'user': user, 'path': red})

    return JsonResponse({"code": count, 'username': user, 'path': '/business/index/'})


@cache_page(60*1)
def logout(request):
    request.session.pop('user')  #
    return redirect('/business/login/')


@cache_page(60*1)
@decorate
def index(request):
    user = request.session.get('user')  #
    return render(request, 'business/index.html', {'username': user})


@cache_page(60*1)
@decorate
def shop(request):
    user = request.session.get('user')  #
    order_list = Border.objects.all()
    return render(request, 'business/order.html', {'username': user, 'order_list': order_list})


@cache_page(60*1)
@decorate
def message(request):
    user = request.session.get('user')  #
    chator = Chat.objects.values('uid__name').distinct()
    no_rend = Chat.objects.filter(sign='0').values('uid__name').annotate(count=Count("sign"))
    # print(chator)
    return render(request, 'business/message.html', {'username': user, 'chator': chator, 'no_rend': no_rend})


@cache_page(60*1)
@decorate
def list(request):
    user = request.session.get('user')  #
    if request.method == "POST":
        search = request.POST.get('search')
        all_item = AllClass.objects.filter(classlist__name__contains=search)
        return render(request, 'business/search.html', {'username': user, 'all_item': all_item})
    all_item = AllClass.objects.all()
    return render(request, 'business/list.html', {'username': user, 'all_item': all_item})


@decorate
def add(request):
    user = request.session.get('user')  #
    lists = ClassList.objects.values('l_number').distinct()
    if request.method == "POST":
        # allclass表
        number = request.POST.get('number', '')
        name = request.POST.get('name', '')
        classlist = request.POST.get('classlist', '')
        if number and name and classlist:
            items = ClassList.objects.get(l_number=classlist)
            AllClass.objects.create(number=number, name=name, classlist=items)
            return redirect('/business/list/')

        # classlist表
        l_number = request.POST.get('l_number')
        cname = request.POST.get('cname')
        img_url = request.POST.get('img_url')
        color = request.POST.get('color')
        price = request.POST.get('price')
        count = request.POST.get('count')
        if l_number and cname and img_url:
            ClassList.objects.create(l_number=l_number, name=cname, img_url=img_url, color=color, price=price, count=count)
            return redirect('/business/add/')
        return HttpResponse('添加失败')
    return render(request, 'business/add.html', {'username': user, 'classlist': lists})


@cache_page(60*1)
@decorate
def update(request):
    user = request.session.get('user')  #
    if request.method == 'POST':
        # allclass表
        id = request.POST.get('id')
        number = request.POST.get('number')
        name = request.POST.get('name')
        # classlist表
        l_number = request.POST.get('l_number')
        cname = request.POST.get('cname')
        img_url = request.POST.get('img_url')
        color = request.POST.get('color')
        price = request.POST.get('price')
        count = request.POST.get('count')
        ClassList.objects.filter(l_number=l_number).update(
            name=cname, img_url=img_url, color=color, price=price, count=count)
        AllClass.objects.filter(id=id).update(number=number, name=name)
        return redirect('/business/list/')
    return render(request, 'business/search.html', {'username': user})


@decorate
def delete(request):
    id = request.GET.get('id')
    AllClass.objects.filter(id=id).delete()
    # user = request.session.get('user')
    # all_item = AllClass.objects.all()
    return redirect('/business/list')
    # return render(request, 'business/list.html', {'username': user, 'all_item': all_item})


@decorate
def search(request):
    user = request.session.get('user')  #
    if request.method == "POST":
        search = request.POST.get('search')
        all_item = AllClass.objects.filter(classlist__name__contains=search)
        return render(request, 'business/search.html', {'username': user, 'all_item': all_item})
    return render(request, 'business/search.html', {'username': user})


@decorate
def active(request):
    return HttpResponse("活动尚未开放")


@cache_page(60*1)
@decorate
def ad(request):
    user = request.session.get('user')  #
    user = Binfo.objects.filter(name=user)
    return render(request, 'business/ad.html', {'username': user})


# def chat(request):
#     message = request.GET.get('message')
#     print(message)
#     return render(request, 'index/chat.html')