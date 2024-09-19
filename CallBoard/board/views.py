from django.contrib.auth import logout, authenticate, login
from django.http import Http404
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView, CreateView

from .models import Image, Video, Post, OneTimeCode, Member
from .forms import UserCreationForm, PostForm


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


def logout_view(request):
    logout(request)
    return redirect('/post/')


class RegisterView(View):
    template_name = 'registration/register.html'

    def get(self, request):
        context = {
            'form': UserCreationForm(),
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=password)
            login(request, user)
            return redirect('/post/')

        context = {
            'form': form
        }
        return render(request, self.template_name, context)




