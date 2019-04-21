from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from Login.models import *
from global_tools.page import Page
from django.views.decorators.cache import cache_page
from django.core.cache import cache


# cache.set('name', 'password', 300)
# name = cache.get('name')

@cache_page(60*10)
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
    no_read = Chat.objects.filter(uid__name=user, sign='0').count()  # 未读消息的数量
    title = AllClass.objects.values('name', 'number').distinct()  # 去重
    Mylist = []
    for i in title:
        message = AllClass.objects.filter(number=i['number']).values(
            'classlist__name', 'classlist__price', 'classlist__img_url', 'classlist__l_number').order_by('-classlist__l_number')[:5]
        Mylist.append([message, i])
    return render(request, 'index/index.html', {"Mylist": Mylist, 'username': user, 'count': count, 'no_read': no_read})


@cache_page(60*10)
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

    # 按价格低到高排序
    if '/list/price/0' in request.path:
        # 后端处理的分页 （页码， 总数， url， 一页展示信息数， 页脚显示页码数）
        page_obj = Page(page, all_count, url_prefix='/list/price/?id=' + name, per_page=12, max_page=3)

        goodslist = AllClass.objects.filter(name=name).values('classlist__name', 'classlist__price',
                                                          'classlist__img_url', 'classlist__see_nums', 'classlist__pay_nums',
                                                          'classlist__l_number').order_by('classlist__price')[
                page_obj.start:page_obj.end]

    # 按价格高到低排序
    elif '/list/price/1' in request.path:
        # 后端处理的分页 （页码， 总数， url， 一页展示信息数， 页脚显示页码数）
        page_obj = Page(page, all_count, url_prefix='/list/price/?id=' + name, per_page=12, max_page=3)

        goodslist = AllClass.objects.filter(name=name).values('classlist__name', 'classlist__price',
                                                              'classlist__img_url', 'classlist__see_nums',
                                                              'classlist__pay_nums',
                                                              'classlist__l_number').order_by('-classlist__price')[
                    page_obj.start:page_obj.end]
    # 人气从低到高
    elif '/list/hot/0' in request.path:

        # 后端处理的分页 （页码， 总数， url， 一页展示信息数， 页脚显示页码数）
        page_obj = Page(page, all_count, url_prefix='/list/?id=' + name, per_page=12, max_page=3)

        goodslist = AllClass.objects.filter(name=name).values('classlist__name', 'classlist__price', 'classlist__img_url',
                                                              'classlist__see_nums', 'classlist__pay_nums',
                                                      'classlist__l_number').order_by('classlist__see_nums')[page_obj.start:page_obj.end]
    # 人气从高到低
    elif '/list/hot/1' in request.path:

        # 后端处理的分页 （页码， 总数， url， 一页展示信息数， 页脚显示页码数）
        page_obj = Page(page, all_count, url_prefix='/list/?id=' + name, per_page=12, max_page=3)

        goodslist = AllClass.objects.filter(name=name).values('classlist__name', 'classlist__price', 'classlist__img_url',
                                                              'classlist__see_nums', 'classlist__pay_nums',
                                                          'classlist__l_number').order_by('-classlist__see_nums')[page_obj.start:page_obj.end]

    # 默认不排序
    else:
        # 后端处理的分页 （页码， 总数， url， 一页展示信息数， 页脚显示页码数）
        page_obj = Page(page, all_count, url_prefix='/list/?id=' + name, per_page=12, max_page=3)

        goodslist = AllClass.objects.filter(name=name).values('classlist__name', 'classlist__price',
                                                              'classlist__img_url', 'classlist__see_nums', 'classlist__pay_nums',
                                                              'classlist__l_number')[page_obj.start:page_obj.end]

    page_html = page_obj.page_html()
    return render(request, 'index/list.html', {"goodsList": goodslist, "name": name, "username": user, "count": count, 'page_html': page_html})


def search(request):
    search = request.GET.get('search')
    list = ClassList.objects.filter(name__icontains=search)
    return render(request, 'index/search.html', {'list': list})


def ticket(request):
    ticket_list = Ticket.objects.all()
    return render(request, 'index/coupon.html', {'ticket': ticket_list})


def ticket_update(request):
    ret = {}
    id = request.GET.get('id')
    name = UserInfo.objects.get(name=request.session.get('user'))
    try:
        Ticket.objects.filter(id=id).update(user=name)
        ret['msg'] = "领取成功"
    except:
        ret['msg'] = "领取失败"
    return JsonResponse(ret)

