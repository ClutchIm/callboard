from django.conf import settings
from django.contrib.auth import logout, login
from django.db.utils import IntegrityError
from django.http import Http404
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.models import Group

from .models import Image, Video, Post, User
# from .forms import PostForm
from .utils import generate_otp, verify_otp, send_email_otp


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


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        news_subscription = request.POST['news_subscription']
        try:
            if news_subscription:
                news_subscription = True
        except KeyError:
            news_subscription = False

        if password1 == password2:
            try:
                user = User.objects.create_user(
                    username=username, email=email, password=password1, news_subscription=news_subscription
                )
            except IntegrityError:
                error_msg = 'Пользователь с таким именем уже существует'
                return render(request, 'registration/register.html', {'msg': error_msg})

            generate_otp(user=user)
            send_email_otp(user=user)

            return redirect('verify_otp', user_id=user.id)

        else:
            error_msg = 'Проверьте правильность написания паролей'
            return render(request, 'registration/register.html', {'msg': error_msg})

    return render(request, 'registration/register.html')


def verify(request, user_id):
    user = User.objects.get(id=user_id)

    if request.method == 'POST':
        email_otp = request.POST['email_otp']

        if verify_otp(otp=email_otp, user=user):
            user.is_verified = True
            user.email_otp = None

            logged_users = Group.objects.get(name='logged_users')
            user.groups.add(logged_users)

            user.save()
            login(request, user)

            return redirect('/post/')
        else:
            msg = 'Пожалуйста проверьте правильность написания кода'
            return render(request, 'registration/verify_otp.html', {'error': msg, 'user': user})

    return render(request, 'registration/verify_otp.html', {'user': user})


