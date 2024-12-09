from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as CustomUserAdmin
from django.contrib.auth import get_user_model
User = get_user_model()
# Register your models here.
@admin.register(User)
class UserAdmin(CustomUserAdmin):
    list_display =['first_name','last_name','email','username']