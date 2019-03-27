"""
装饰器 验证登录
"""

from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from functools import wraps


def login(func):
    @wraps(func)
    def login_fun(request, *args, **kwargs):
        if request.session.get('user'):
            return func(request, *args, **kwargs)
        else:
            red = redirect('/login/')
            red.set_cookie('url', request.path)  # 把路径存到cookies中, 方便后面用
            return red
    return login_fun
