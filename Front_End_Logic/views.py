from django.shortcuts import render
from django.http import JsonResponse
from API.models import WildLife
from django.views import View
import json
from .forms import ImageForm
# Create your views here.

def homepage(request):
    context = {}
    return render(request,'Front_End_Logic/index.html',context)





def create_image_view(request):
    if request.method == 'POST':
        form = ImageForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return JsonResponse({'message': 'Image created successfully!'}, status=201)
        return JsonResponse({'message': 'Failed to create image', 'errors': form.errors}, status=400)
    else:
        # Initialize the form for GET requests
        form = ImageForm()
        return render(request, 'Front_End_Logic/create_image.html', {'form': form})


class SignupPageView(View):
    def get(self, request):
        return render(request, 'Front_End_Logic/signup.html')