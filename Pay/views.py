from django.shortcuts import render


def pay(request):
    return render(request, 'pay/pay.html')
