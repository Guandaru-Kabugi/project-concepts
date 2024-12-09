from rest_framework import serializers
from .models import WildLife


class WildLifeSerializer(serializers.ModelSerializer):

    class Meta:
        model = WildLife
        fields = ['id','slug_field','name','page_location','section','image_url','image']