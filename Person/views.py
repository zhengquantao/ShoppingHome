from django.shortcuts import render
from Login.models import UserInfo


def person(request):
    user = request.session.get('user')
    ret_user = UserInfo.objects.filter(name=user).first()
    # print(ret_user.name)
    return render(request, 'person/person.html', {"user": ret_user})
