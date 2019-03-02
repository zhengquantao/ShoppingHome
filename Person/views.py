from django.shortcuts import render


def person(request):
    return render(request, 'person.html')
