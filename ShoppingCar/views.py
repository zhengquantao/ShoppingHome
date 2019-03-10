from django.shortcuts import render
from django.http import JsonResponse


def shoppingCar(request):
    try:
        user = request.ssession.get('user')
    except:
        user = 0
    if not user:
        return JsonResponse({"code": 0})
    print(user)
    return JsonResponse({"code": 1})
