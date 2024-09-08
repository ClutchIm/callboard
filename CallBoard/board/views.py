from django.http import Http404
from django.shortcuts import render

from .models import Image


# Create your views here.

def image(request, image_id):
    image = Image.objects.get(pk=image_id)
    if image is not None:
        return render(request, 'image.html', {'image': image})
    else:
        return Http404('Image not found')
