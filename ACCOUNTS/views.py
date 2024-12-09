from django.shortcuts import render,get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer
from rest_framework.generics import CreateAPIView
from rest_framework.decorators import api_view
from django.contrib.auth import get_user_model
# Create your views here.
User = get_user_model()


class CreateNewUser(CreateAPIView):
    serializer_class = UserSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = get_object_or_404(User,email=request.data['email'])
            user.set_password(request.data['password'])
            user.save()
            return Response({"User": serializer.data},status=status.HTTP_200_OK)
        else:
            return Response({"errors":serializer.errors},status=status.HTTP_400_BAD_REQUEST)
# log in


@api_view(['POST'])
def login(request):
    user = get_object_or_404(User,email=request.data['email'])
    if user:
        if user.check_password(request.data['password']):
            serializer = UserSerializer(instance=user)
            return Response({"user":serializer.data},status=status.HTTP_200_OK)
        else:
            return Response({"errors":serializer.errors},status=status.HTTP_401_UNAUTHORIZED)
        
    