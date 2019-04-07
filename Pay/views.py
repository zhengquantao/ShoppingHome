from django.shortcuts import render, HttpResponse, redirect
from global_tools.pay import AliPay
import time
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from global_tools.login_decorate import login
from Login.models import Pay, UserInfo, ClassList, Car, Border, Ticket
from django.http import JsonResponse


# @login
def aliPay():
    obj = AliPay(
        appid=settings.APPID,
        app_notify_url=settings.NOTIFY_URL,  # 如果支付成功， 支付宝想这个地址发送POST请求（效验是否支付已经完成）
        return_url=settings.RETURN_URL,  # 如果支付成功， 重定向到你的网站位置
        alipay_public_key_path=settings.PUB_KEY_PATH,  # 支付宝公钥
        app_private_key_path=settings.PRI_KEY_PATH,  # app应用私钥
        debug=True,  # 默认False
    )
    return obj


# 请求中转
# @login
def pay(request):
    price = request.GET.get('price')
    user = request.session.get('user')  #
    item = request.GET.get('item')
    # print(item)
    ticket = Ticket.objects.filter(user__name=user).values('tName', 'tPrice', 'tDescribe')
    return render(request, 'pay/pay.html', {'price': price, 'username': user, 'item': item, 'ticket': ticket})


def pay_ali(request):
    price = float(request.GET.get('price'))
    # user = request.session.get('user')
    item = request.GET.get('item')
    coupon = request.GET.get('name')
    request.session['item'] = item  # 把商品信息存到session里
    if coupon:
        request.session['coupon'] = coupon
    # return HttpResponse('OK')

    alipay = aliPay()  # 调用上面的信息

    # price = float(request.POST.get('price'))
    out_trade_no = 'x2' + str(time.time())
    # 价格，购买的商品加密
    # 拼接成URL
    query_params = alipay.direct_pay(
        subject=item,  # 商品简单描述
        # item_message=item,  # 商品信息
        out_trade_no=out_trade_no,  # 商户订单号
        total_amount=price,  # 交易金额（单位: 元 保留两位小数）
    )

    pay_url = "https://openapi.alipaydev.com/gateway.do?{}".format(query_params)

    return redirect(pay_url)


def pay_wx(request):
    return HttpResponse("暂不开放")


def pay_yl(request):
    return HttpResponse("暂不开放")


def pay_result(request):
    """
    支付完成， 跳转会的地址
    :param request:
    :return:
    """
    params = request.GET.dict()
    sign = params.pop('sign', None)

    alipay = aliPay()

    status = alipay.verify(params, sign)

    if status:
        return HttpResponse('支付成功')
    return HttpResponse('支付失败')


@csrf_exempt
def update_order(request):
    """
    支付成功后，支付宝向该地址发送的POST请求（用于修改订单状态）
    :param request:
    :return:
    """
    print("成功了哦！")
    if request.method == 'POST':
        from urllib.parse import parse_qs

        body_srt = request.body.decode('utf-8')
        post_data = parse_qs(body_srt)

        post_dict = {}
        for k, v in post_data.items():
            post_dict[k] = v[0]

        alipay = aliPay()

        sign = post_dict.pop('sign', None)
        status = alipay.verify(post_dict, sign)
        if status:
            # 修改订单状态
            out_trade_no = post_dict.get('out_trade_no')
            print('订单状态：', out_trade_no)
            # 2. 根据订单号将数据库中的数据进行更新

            return HttpResponse('支付成功')
        else:
            return HttpResponse('支付失败')

    return HttpResponse('')


# 支付成功进来
def update_status(request):
    trade_no = request.GET.get('out_trade_no')  # 订单号
    print(trade_no)
    user = request.session.get('user')
    # 删除已使用的优惠劵
    coupon = request.session.get('coupon')
    Ticket.objects.filter(user__name=user, tName=coupon).delete()

    user_obj = UserInfo.objects.get(name=user)  # 得到对象参数信息
    items = request.session.get('item')  # 取出商品信息
    item_list = items.split(',')
    num = len(item_list)//4
    for i in range(num):
        item_id = item_list[i*4+1]
        item_num = item_list[i*4+2]
        # print(item_id, item_num)
        item_id_obj = ClassList.objects.get(l_number=item_id)
        item_id_obj.count -= int(item_num)  # 库存 减掉已卖出的数量
        item_id_obj.pay_nums += int(item_num)  # 销售量加
        item_id_obj.save()
        Pay.objects.create(p_user=user_obj, c_item=item_id_obj, trade_no=trade_no[:16], count=int(item_num), success=1)
        try:
            Car.objects.filter(class_item=item_id).delete()
            trade_item = Pay.objects.get(trade_no=trade_no[:16])  # 获取pay表的对象
            Border.objects.create(pay=trade_item, item_no=trade_no[:16])  # 订单数据加入到business表中
        except:
            pass
    request.session.pop('item')

    return redirect('/person/order/')
