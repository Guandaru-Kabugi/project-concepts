from django.urls import path

from . import views

urlpatterns = [
    path('create_image/',views.CreateNewImage.as_view(),name='new_image'),
    path('list_image/',views.ListImages.as_view(),name='list_images'),
    path('get_image/<slug:slug>/',views.GetOneImage.as_view(),name='get_image'),
    
] 

