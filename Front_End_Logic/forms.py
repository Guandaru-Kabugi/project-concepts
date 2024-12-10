from django import forms
from API.models import WildLife

class ImageForm(forms.ModelForm):

    class Meta:
        model = WildLife
        fields = ['name','page_location','section','image_url','image']