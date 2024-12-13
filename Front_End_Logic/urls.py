from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
urlpatterns = [
    path('home/',views.homepage,name='home'),
    path('create_image/', views.create_image_view, name='create_newimage'),
    path('signup-page/', views.SignupPageView.as_view(), name='signup-page'),
    path('post_today_image/',views.get_ig_image,name='today')
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
