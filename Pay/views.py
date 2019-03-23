from django.shortcuts import render, HttpResponse, redirect
from global_tools.pay import AliPay
import time
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse


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
def pay(request):
    price = request.GET.get('price')
    user = request.session.get('user')  #
    item = request.GET.get('item')
    # print(item)
    return render(request, 'pay/pay.html', {'price': price, 'username': user, 'item': item})


def pay_ali(request):
    price = float(request.GET.get('price'))
    user = request.session.get('user')  #
    item = request.GET.get('item')
    # return HttpResponse('OK')

    alipay = aliPay()  # 调用上面的信息

    # price = float(request.POST.get('price'))
    out_trade_no = 'x2' + str(time.time())
    # 价格，购买的商品加密
    # 拼接成URL
    query_params = alipay.direct_pay(
        subject=item,  # 商品简单描述
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
            print(out_trade_no)
            # 2. 根据订单号将数据库中的数据进行更新

            return HttpResponse('支付成功')
        else:
            return HttpResponse('支付失败')
    return HttpResponse('')