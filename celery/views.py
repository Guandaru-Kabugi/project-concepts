from django.shortcuts import render

# Create your views here.


def messageboard(request):
    return render(request,'celery/messageboard.html')