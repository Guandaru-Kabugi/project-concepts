from django.shortcuts import render
from django.http import JsonResponse
from API.models import WildLife
from django.views import View
import json
from .forms import ImageForm
from datetime import datetime
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_KEY = os.getenv("INST_API_KEY")
IG_ID = os.getenv("INSTAGRAM_BUSINESS_ACCOUNT_ID")

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
    

# we post a specific image of the day on homepage
def get_ig_image(request):
    # Get today's date
    today = datetime.today().strftime("%Y-%m-%d")

    # Convert today's date to Unix timestamp
    date_obj = datetime.strptime(today, "%Y-%m-%d")
    since = int(date_obj.timestamp())
    until = int(date_obj.timestamp() + 86400)  # End of the day

    # Fetch Instagram posts
    url = f"https://graph.facebook.com/v21.0/{IG_ID}/media"
    params = {
        "fields": "id,caption,media_type,media_url,timestamp",
        "access_token": API_KEY,
        "since": since,
        "until": until,
    }

    response = requests.get(url, params=params)
    posts = []
    if response.status_code == 200:
        posts = response.json().get("data", [])

    # Render the homepage template with the posts
    return render(request, "Front_End_Logic/get_image.html", {"posts": posts})