from django.http import Http404
from django.shortcuts import render

from .models import Image


# Create your views here.

def image(request, image_id):
    images = Image.objects.get(pk=image_id)
    if images is not None:
        return render(request, 'image.html', {'image': images})
    else:
        return Http404('Image not found')
