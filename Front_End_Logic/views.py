from django.shortcuts import render
from django.http import JsonResponse
from API.models import WildLife
import json
# Create your views here.

def homepage(request):
    context = {}
    return render(request,'Front_End_Logic/index.html',context)



def create_image_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            # Extract fields
            name = data.get('name')
            page_location = data.get('page_location')
            section = data.get('section')
            image_url = data.get('image_url')
            image = data.get('image')

            # Validation
            if not name or not slug or not page_location or not image or not image_url:
                return JsonResponse({"errors": "All fields are required."}, status=400)

            # Save to database
            new_image = WildLife(
                name=name,
                page_location=page_location,
                section=section,
                image_url=image_url,
                image=image
            )
            new_image.save()

            return JsonResponse({"message": "Image created successfully."}, status=200)

        except Exception as e:
            return JsonResponse({"errors": str(e)}, status=400)

    return JsonResponse({"errors": "Invalid request method."}, status=405)
