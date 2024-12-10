from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
urlpatterns = [
    path('home/',views.homepage,name='home'),
    path('create_image/', views.create_image_view, name='create_newimage'),
    path('signup-page/', views.SignupPageView.as_view(), name='signup-page'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
