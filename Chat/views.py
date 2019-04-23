from django.shortcuts import render
from django.http import JsonResponse
from Login.models import Chat, UserInfo, Binfo
from global_tools.login_decorate import login
from django.views.decorators.cache import cache_page
# from dwebsocket.decorators import accept_websocket
from django.core import serializers
import json
import time


# 聊天
@login
def chat(request):
    user = request.session.get('user')
    to = request.GET.get('to')

    if not to:  # 如果没有to 说明是用户发送的消息
        message_list = Chat.objects.filter(uid__name=user)
        Chat.objects.filter(uid__name=user).update(sign='1')  # 把未读改成已读
    else:  # 有就是商家发的消息
        message_list = Chat.objects.filter(uid__name=to)
        Chat.objects.filter(uid__name=to).update(sign='1')  # 把未读改成已读
        # print('list:', message_list)
    request.session['count_comment'] = message_list.count()  # 把消息量记起来
    return render(request, 'index/chat.html', {'username': user, 'message_list': message_list, 'to': to})


# 把数据存入数据库
def update(request):
    message = request.GET.get('message')
    user = request.GET.get('user')  # 谁发的
    to = request.GET.get('to')  # 要发送给谁的
    # buser = request.session.get('bUser')

    if user and user != 'a':
        bid = Binfo.objects.get(name='a')
        uid = UserInfo.objects.get(name=user)
        # print('用户发送的：', uid, bid)
        Chat.objects.create(bid=bid, uid=uid, content=message, who_send=0, sign=0)
    else:
        bid = Binfo.objects.get(name='a')
        uid = UserInfo.objects.get(name=to)
        # print('商家发送的：', bid, uid)
        Chat.objects.create(bid=bid, uid=uid, content=message, who_send=1, sign=0)
    # request.session['count_comment'] = Chat.objects.filter(uid__name=uid).count()
    return JsonResponse({})


# 把数据从数据库取出放回到页面上
@cache_page(2)
def change(request):
    user = request.GET.get('user')
    to = request.GET.get('to')
    count = request.session.get('count_comment')
    # print('1', user, '2', to)
    dict_message = {}
    if user == "" and to == "":
        return JsonResponse({})

    elif to == 'None':  # 判断是不是用户的请求
        if count != Chat.objects.filter(uid__name=user).count():
            request.session['count_comment'] = Chat.objects.filter(uid__name=user).count()
            message = Chat.objects.filter(uid__name=user).last()  # 取最后一个
            if message.who_send == '1':  # 如果最后一个是商家发的就要
                dict_message['content'] = message.content
                dict_message['who_send'] = message.who_send
                dict_message['date'] = str(message.date)
            else:  # 不是就抛出
                return JsonResponse({})
        else:
            return JsonResponse({"status": 1})

    else:  # 商家发的请求
        if count != Chat.objects.filter(uid__name=to).count():
            request.session['count_comment'] = Chat.objects.filter(uid__name=to).count()
            message = Chat.objects.filter(uid__name=to).last()
            if message.who_send == '0':
                dict_message['content'] = message.content
                dict_message['who_send'] = message.who_send
                dict_message['date'] = str(message.date)
            else:
                return JsonResponse({})

        else:
            return JsonResponse({"status": 1})

    # one_message = serializers.serialize('json', message)  # 将queryset对象转成json格式
    # print(one_message)
    # one_message = json.dumps(dict_message)  # 将json转成字典
    # print(type(one_message))
    return JsonResponse(dict_message)


# websocket
# @accept_websocket
# def web_socket(request):
#     if not request.is_websocket():
#         return render(request, 'index/websocket.html')
#     else:
#         print(request.websocket.wait())
#         # request.websocket.wait()
#         request.websocket.send("收到了".encode('utf-8'))
        # request.websocket.close()


