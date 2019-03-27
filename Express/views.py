from django.shortcuts import render

# Create your views here.


def express(request):
    return render(request, 'person/express.html')