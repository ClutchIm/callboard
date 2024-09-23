from lib2to3.fixes.fix_input import context

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import logout, login
from django.db.utils import IntegrityError
from django.http import Http404
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import Group

from .models import Image, Video, Post, User, Comment
from .forms import PostForm, ImageFormSet, VideoFormSet
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

# TODO: сделать поиск
class PostListView(ListView):
    model = Post
    ordering = '-time_in'
    template_name = 'posts.html'
    context_object_name = 'post'
    paginate_by = 12

# TODO: добавить список верифицированных комментариев
class PostDetailView(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


class PostInline():
    form_class = PostForm
    model = Post
    template_name = "post_create_or_update.html"

    def form_valid(self, form):
        named_formsets = self.get_named_formsets()
        if not all((x.is_valid() for x in named_formsets.values())):
            return self.render_to_response(self.get_context_data(form=form))

        self.object = form.save()

        # для каждого набора форм попытаться найти определенную функцию
        # сохранения набора форм, в противном случае просто сохранить
        for name, formset in named_formsets.items():
            formset_save_func = getattr(self, 'formset_{0}_valid'.format(name), None)
            if formset_save_func is not None:
                formset_save_func(formset)
            else:
                formset.save()
        return redirect('PostList')

    def formset_video_valid(self, formset):
        """
            Триггер для сохранения формсета видео.
        """
        video = formset.save(commit=False)
        for obj in formset.deleted_objects:
            obj.delete()
        for vid in video:
            vid.post = self.object
            vid.save()

    def formset_images_valid(self, formset):
        """
            Триггер для сохранения формсета изображений.
        """
        images = formset.save(commit=False)
        for obj in formset.deleted_objects:
            obj.delete()
        for image in images:
            image.product = self.object
            image.save()

# TODO: Закончить патерн, сделать форму, посмотреть как ее добавить с учетом фото и видео
class PostCreateView(PostInline ,CreateView):
    permission_required = ('board.add_post',)

    def get_context_data(self, **kwargs):
        ctx = super(PostCreateView, self).get_context_data(**kwargs)
        ctx['named_formsets'] = self.get_named_formsets()
        return ctx

    def get_named_formsets(self):
        if self.request.method == "GET":
            return {
                'video': VideoFormSet(prefix='video'),
                'images': ImageFormSet(prefix='images'),
            }
        else:
            return {
                'video': VideoFormSet(self.request.POST or None, self.request.FILES or None, prefix='video'),
                'images': ImageFormSet(self.request.POST or None, self.request.FILES or None, prefix='images')
            }


class PostUpdateView(UpdateView):
    permission_required = ('board.change_post',)

    def get_context_data(self, **kwargs):
        ctx = super(PostUpdateView, self).get_context_data(**kwargs)
        ctx['named_formsets'] = self.get_named_formsets()
        return ctx

    def get_named_formsets(self):
        return {
            'video': VideoFormSet(
                self.request.POST or None,
                self.request.FILES or None,
                instance=self.object,
                prefix='videos'
            ),

            'images': ImageFormSet(
                self.request.POST or None,
                self.request.FILES or None,
                instance=self.object,
                prefix='images'
            ),
        }

# TODO: сделать патерн
class PostDeleteView(DeleteView):
    permission_required = ('board.delete_post',)
    model = Post
    template_name = 'post_delete.html'


def delete_image(request, pk):
    try:
        image = Image.objects.get(id=pk)
    except Image.DoesNotExist:
        messages.success(
            request, 'Изображение не найдено'
            )
        return redirect('update_post', pk=image.post.id)

    image.delete()
    messages.success(
            request, 'Изображение удаленно'
            )
    return redirect('update_post', pk=image.product.id)


def delete_video(request, pk):
    try:
        video = Video.objects.get(id=pk)
    except Video.DoesNotExist:
        messages.success(
            request, 'Видео не найдено'
            )
        return redirect('update_post', pk=video.product.id)

    video.delete()
    messages.success(
            request, 'Видео удалено'
            )
    return redirect('update_post', pk=video.product.id)

# TODO: Когда добавлю комменты и посты доработать
class PersonalOfficeView(ListView):
    model = Comment
    template_name = 'personal_office.html'
    context_object_name = 'comments'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user


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


