from django.shortcuts import render,get_object_or_404
from .serializers import WildLifeSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from datetime import datetime
from rest_framework.generics import CreateAPIView,ListAPIView,RetrieveAPIView
from .models import WildLife
import requests
# Create your views here.
from dotenv import load_dotenv
import os
load_dotenv()
API_KEY = os.getenv('INST_API_KEY')
IG_ID = os.getenv('INSTAGRAM_BUSINESS_ACCOUNT_ID')

#create
class CreateNewImage(CreateAPIView):
    serializer_class = WildLifeSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Image":serializer.data},status=status.HTTP_200_OK)
        else:
            return Response({"errors":serializer.errors},status=status.HTTP_400_BAD_REQUEST)
        
#list
class ListImages(ListAPIView):
    serializer_class = WildLifeSerializer
    queryset = WildLife.objects.all()

#detail
class GetOneImage(RetrieveAPIView):
    serializer_class = WildLifeSerializer
    def get(self, request, slug):

        object = get_object_or_404(WildLife,slug_field=slug)
        if object:
            serializer = self.get_serializer(instance = object)
            return Response({"image":serializer.data},status=status.HTTP_200_OK)
        else:
            return Response({"errors":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        

#We create api for getting images from instagram
class ImageAccessAPI(APIView):
    def get(self,request):
         url = f"https://graph.facebook.com/v21.0/{IG_ID}/media"
         params = {
             "fields":"id,caption,media_type,media_url,timestamp",
             "access_token":API_KEY
         }
         response = requests.get(url,params=params)
         if response.status_code == 200:
             return Response(response.json(),status=status.HTTP_200_OK)
         return Response(response.json(),status=response.status_code)
    
    #try posting an image
    def post(self, request, *args, **kwargs):
        url = f"https://graph.facebook.com/v21.0/{IG_ID}/media"
        data = request.data #will have caption and image url
        if 'image_url' not in data or 'caption' not in data:
            return Response({"errors":"image_url and caption are required fields"},status=status.HTTP_400_BAD_REQUEST)
        #create container to store the data
        container_url = f'{url}'
        container_payload = {
             "image_url": data["image_url"],
            "caption": data["caption"],
            "access_token": API_KEY,
        }
        container_response = requests.post(container_url,data=container_payload)
        if container_response.status_code != 200:
            return Response(container_response.json,status=container_response.status_code)
        container_id = container_response.json().get('id')

        #publish the data

        publish_url = f"https://graph.facebook.com/v21.0/{IG_ID}/media_publish"
        publish_payload = {"creation_id": container_id, "access_token": API_KEY}
        publish_response = requests.post(publish_url, data=publish_payload)

        if publish_response.status_code == 200:
            return Response(publish_response.json(), status=status.HTTP_201_CREATED)
        return Response(publish_response.json(), status=publish_response.status_code)

class GetSpecificImage(APIView):
    def get(self, request):
                # Retrieve date from query parameters 
        specific_date = request.query_params.get("date") # I am trying to get the data by passing it as a query
        if not specific_date:
            return Response(
                {"error": "Please provide a date in the format YYYY-MM-DD"},
                status=status.HTTP_400_BAD_REQUEST,
            )
#we use try and except block here to fetch the date
        try:
            # Convert the provided date to Unix timestamp (since/until require timestamps)
            date_obj = datetime.strptime(specific_date, "%Y-%m-%d")
            since = int(date_obj.timestamp())
            until = int((date_obj.timestamp() + 86400))  # Add 24 hours to get the end of the day
        except ValueError:
            return Response(
                {"error": "Invalid date format. Use YYYY-MM-DD"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Make the API call with date filters
        url = f"https://graph.facebook.com/v21.0/{IG_ID}/media"
        params = {
            "fields": "id,caption,media_type,media_url,timestamp",
            "access_token": API_KEY,
            "since": since,
            "until": until,
        }
        response = requests.get(url, params=params)

        # Handle the API response
        if response.status_code == 200:
            return Response(response.json(), status=status.HTTP_200_OK)
        return Response(response.json(), status=response.status_code)