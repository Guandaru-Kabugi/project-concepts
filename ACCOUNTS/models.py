from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager

# Create your models here.

class UserManager(BaseUserManager):
    def create_user (self,email,username,first_name,last_name,password=None):
        if not email:
            raise ValueError('email is required')
        if not username:
            raise ValueError('username is required')
        if not first_name:
            raise ValueError('first name is required')
        if not last_name:
            raise ValueError('last name is required')
        user = self.model(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self,email,username,first_name,last_name,password=None):
        user = self.create_user(email,password=password,username=username,first_name=first_name,last_name=last_name)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
class CustomUser(AbstractUser):
    email = models.EmailField(max_length=200,unique=True,null=False,verbose_name='Email Address')
    username = models.CharField(max_length=50,unique=True,null=False,verbose_name='username')
    first_name = models.CharField(max_length=100,unique=False,null=False,verbose_name='First Name')
    last_name = models.CharField(max_length=100,unique=False,null=False,verbose_name='Last Name')


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','first_name','last_name']

    objects = UserManager()

    def __str__(self):
        return self.username