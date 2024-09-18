from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView

from .models import Image, Video, Post, OneTimeCode, Member
# from .forms import CustomSignupForm, PostForm


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
    paginate_by = 12


class PostDetailView(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


# class RegisterView(CreateView):
#     model = User
#     form_class = CustomSignupForm
#     success_url = '/login'
#     template_name = 'registration/register.html'






