from django.db import models
from django.utils.text import slugify

# Create your models here.
# model schema that allows saving of images into database


class WildLife(models.Model):
    name = models.CharField(max_length=100,unique=True,null=False,verbose_name='name of image')
    page_location = models.CharField(max_length=50,unique=False,null=False,verbose_name='Page Where Image is/was Located')
    section = models.CharField(max_length=50,unique=False,null=False,verbose_name='Part of the page where Image is located')
    image_url = models.URLField(max_length=300,unique=True,null=True,verbose_name='link of the image')
    image = models.ImageField(verbose_name='Image',upload_to='wildlife/')
    slug_field = models.SlugField(unique=True,null=True,verbose_name='slug field',max_length=100,blank=True)


    def __str__(self):
        return self.slug_field
    
    def save(self, *args, **kwargs):
        if not self.slug_field:
            self.slug_field = slugify(self.name)

        return super().save(*args, **kwargs)

