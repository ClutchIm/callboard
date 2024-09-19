from django.conf import settings
from django.contrib.auth import logout, authenticate, login
from django.http import Http404
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView, CreateView
from django.core.mail import send_mail

from .models import Image, Video, Post, User
from .forms import UserCreationForm, PostForm
from .utils import generate_otp, verify_otp


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


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        user = User.objects.create_user(username=username, email=email, password=password)

        # Generate and save OTPs
        email_otp = generate_otp()
        user.email_otp = email_otp
        user.save()

        # Send email OTP
        send_mail(
            'Email Verification OTP',
            f'Your OTP for email verification is: {email_otp}',
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )

        return redirect('verify_otp', user_id=user.id)

    return render(request, 'registration/register.html')


def verify(request, user_id):
    user = User.objects.get(id=user_id)

    if request.method == 'POST':
        email_otp = request.POST['email_otp']

        if verify_otp(email_otp, user.email_otp):
            user.is_email_verified = True
            user.email_otp = None
            user.save()
            login(request, user)
            return redirect('/post/')
        else:
            return render(request, 'registration/verify_otp.html', {'error': 'Invalid OTP'})

    return render(request, 'registration/verify_otp.html')


