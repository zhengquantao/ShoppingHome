from django.shortcuts import render
from Login.models import SecKill, ClassList
from django.core.cache import cache
# from django.core.serializers import serialize
from django.http import HttpResponse, JsonResponse
from global_tools.login_decorate import login
import time
import uuid


#  一开始导入数据
def inRedis(request):
    goods_list = SecKill.objects.all().values('goods__l_number', 'goods__img_url', 'goods__name', 'goods__price', 'goods__count',
                                              'startTime', 'endTime')
    item_list = []
    for good in goods_list:
        cache.set(good['goods__l_number'], good, 60*60)  # 放入cache
        item_list.append(good['goods__l_number'])
    cache.set('item_list', item_list, 60*60)
    return HttpResponse("加入了")


# 秒杀
def seckill(request):
    item_lists_message = []
    trend_path = ''
    item_list_num = cache.get('item_list')
    for item in item_list_num:
        one_item = cache.get(item)
        startTime = time.mktime(one_item['startTime'].timetuple())  # 开始时间
        endTime = time.mktime(one_item['endTime'].timetuple())  # 结束时间
        if startTime > time.time():
            status = 1  # 未开始
        elif endTime < time.time():
            status = 2  # 已结束
        else:
            status = 0  # 进行中
            if not cache.has_key('trend_path'):  # 动态生成接口防止用户恶盗刷
                trend_path = uuid.uuid4()  # 生成动态路径  防止恶意盗刷
                cache.set('trend_path', trend_path, 60*60)
            else:
                trend_path = cache.get('trend_path')
        item_lists_message.append([one_item, status, startTime, endTime])
    return render(request, 'index/seckill.html', {'item_lists_message': item_lists_message, 'trend_path': trend_path})


# 逻辑区
# @login
def sendKill(request):
    goods_id = request.POST.get('id')
    path = request.POST.get('trend_path')
    # print(goods_id, type(path), type(cache.get('trend_path')))
    if not cache.has_key('trend_path'):  # 没有说明活动没有开放
        ret = {"msg": "秒杀失败"}
        return JsonResponse(ret)
    if path != str(cache.get('trend_path')):
        ret = {"msg": "秒杀失败"}
        return JsonResponse(ret)  # 不相等说明是恶意用户
    # print(goods_id)

    user = request.session.get('user')
    if not user:  # 判断是否是登录的
        ret = {"path": "/login/", "msg": "秒杀失败"}
        return JsonResponse(ret)

    goods_id_item = cache.get(goods_id)  # 拿到这个商品的信息
    goods_id_item_count = goods_id_item['goods__count']  # 从缓存中拿到该商品的数量
    goods_id_item_startTime = time.mktime(goods_id_item['startTime'].timetuple())  # 获取活动开始时间
    goods_id_item_endTime = time.mktime(goods_id_item['endTime'].timetuple())  # 获取活动结束时间
    if goods_id_item_count > 0 and goods_id_item_startTime < time.time() < goods_id_item_endTime:  # 防止活动尚未开始就有人来刷
        goods_id_item_count -= 1
        # print(goods_id_item_count)
        ClassList.objects.filter(l_number=goods_id).update(count=goods_id_item_count)  # 更新商品的信息
        goods = SecKill.objects.filter(goods__l_number=goods_id).values('goods__l_number', 'goods__img_url', 'goods__name', 'goods__price', 'goods__count',
                                              'startTime', 'endTime')
        cache.set(goods_id, goods[0], 60*60)  # 更新redis中的信息

        cache.set(request.session.get('user')+'x', goods_id, 60*5)  # 存5分钟让用户支付， 5分钟用户不支付就秒杀失败
        ret = {"path": "/seckill/goodkill/", "msg": "秒杀成功！正在跳转"}
        return JsonResponse(ret)
    else:
        ret = {"msg": "秒杀失败"}
        return JsonResponse(ret)


@login
def goodkill(request):
    goods_id = cache.get(request.session.get('user')+'x')  # 拿出秒杀的商品id
    time_out = cache.ttl(request.session.get('user')+'x')  # 查看过期时间
    item_message = cache.get(goods_id)
    return render(request, 'index/goodkill.html', {"item_message": item_message, "time_out": time_out})