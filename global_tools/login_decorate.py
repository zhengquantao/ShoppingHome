"""
装饰器 验证登录
"""

from django.shortcuts import  redirect
from django.http import HttpResponseRedirect
from functools import wraps


def login(func):
    @wraps(func)
    def login_fun(request, *args, **kwargs):
        users = request.GET.get('user')
        if request.session.get(users):
            return func(request, *args, **kwargs)
        else:
            red = HttpResponseRedirect('/login/')
            red.set_cookie('url', request.get_full_path())
            return red
    return login_fun