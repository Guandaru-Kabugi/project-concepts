from django.shortcuts import render,get_object_or_404
from .serializers import WildLifeSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import CreateAPIView,ListAPIView,RetrieveAPIView
from .models import WildLife
# Create your views here.


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
        

