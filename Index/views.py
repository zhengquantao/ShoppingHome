from django.shortcuts import render, HttpResponse
from Login.models import *
from global_tools.page import Page
from django.views.decorators.cache import cache_page
from django.core.cache import cache


def index(request):
    # user = request.GET.get('user')  #
    # print('------', request.user)
    # print(request.session.get('user'))
    user = request.session.get('user')  #
    if user:
        count = Car.objects.filter(user=user).count()
        if count:
            count = count
    else:
        user = ''
        count = ''

    title = AllClass.objects.values('name', 'number').distinct()
    Mylist = []
    for i in title:
        message = AllClass.objects.filter(number=i['number']).values(
            'classlist__name', 'classlist__price', 'classlist__img_url', 'classlist__l_number')[0:5]
        Mylist.append([message, i])
    return render(request, 'index/index.html', {"Mylist": Mylist, 'username': user, 'count': count})


def list(request):
    name = request.GET.get('id')  # 商品名
    # user = request.GET.get('user')  #
    page = request.GET.get('page')  # 页码
    num = request.GET.get('num')  # 数量
    user = request.session.get('user')  #
    if user:
        count = Car.objects.filter(user=user).count()
        if count:
            count = count

    else:
        count = ''
        user = ''
    all_count = AllClass.objects.filter(name=name).count()

    # 按价格排序
    if '/list/price/' in request.path:
        # 后端处理的分页 （页码， 总数， url， 一页展示信息数， 页脚显示页码数）
        page_obj = Page(page, all_count, url_prefix='/list/price/?id=' + name, per_page=12, max_page=3)

        goodslist = AllClass.objects.filter(name=name).values('classlist__name', 'classlist__price',
                                                          'classlist__img_url',
                                                          'classlist__l_number').order_by('classlist__price')[
                page_obj.start:page_obj.end]

    elif '/list/' in request.path:

        # 后端处理的分页 （页码， 总数， url， 一页展示信息数， 页脚显示页码数）
        page_obj = Page(page, all_count, url_prefix='/list/?id=' + name, per_page=12, max_page=3)

        goodslist = AllClass.objects.filter(name=name).values('classlist__name', 'classlist__price', 'classlist__img_url',
                                                          'classlist__l_number')[page_obj.start:page_obj.end]

    # 默认不排序
    else:
        # 后端处理的分页 （页码， 总数， url， 一页展示信息数， 页脚显示页码数）
        page_obj = Page(page, all_count, url_prefix='/list/?id=' + name, per_page=12, max_page=3)

        goodslist = AllClass.objects.filter(name=name).values('classlist__name', 'classlist__price',
                                                              'classlist__img_url',
                                                              'classlist__l_number')[page_obj.start:page_obj.end]

    page_html = page_obj.page_html()
    return render(request, 'index/list.html', {"goodsList": goodslist, "name": name, "username": user, "count": count, 'page_html': page_html})

