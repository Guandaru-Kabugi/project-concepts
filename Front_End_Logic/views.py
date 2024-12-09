from django.shortcuts import render

# Create your views here.

def homepage(request):
    context = {}
    return render(request,'Front_End_Logic/index.html',context)