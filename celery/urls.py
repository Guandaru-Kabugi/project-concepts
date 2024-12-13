from django.urls import path
from . import views
urlpatterns = [
    path('work_with_celery/',views.messageboard,name='celery')
]
