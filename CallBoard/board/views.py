from django.http import Http404
from django.shortcuts import render
from django.views.generic import ListView

from .models import Image, Video, Post


# Create your views here.

def image(request, image_id):
    images = Image.objects.get(pk=image_id)
    if images is not None:
        return render(request, 'image.html', {'image': images})
    else:
        return Http404('Image not found')


def video(request):
    vid = Video.objects.all()
    return render(request, 'video.html', {'videos': vid})


class PostListView(ListView):
    model = Post
    ordering = '-time_in'
    template_name = 'posts.html'
    context_object_name = 'post'
    paginate_by = 10


