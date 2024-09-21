from django.contrib.auth.models import AbstractUser
from django.db import models
from embed_video.fields import EmbedVideoField
import random
from django.utils.translation import gettext_lazy as _

from .resources import CATEGORY_CHOICE


class User(AbstractUser):

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)
    email_otp = models.CharField(max_length=6, blank=True, null=True)
    user_response = models.BooleanField(default=True, verbose_name="Уведомление об откликах")
    news_subscription = models.BooleanField(default=False, verbose_name="Новостная рассылка")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return f'{self.username}'


# class Member(models.Model):
#     """
#         Модель пользователя, содержащее поля:
#
#         user - поле связанное напрямую с моделью User
#         user_response - булево поле обозначающее согласие
#     на отправку уведомлений на e-mail об ответе на отклик
#     по дефолту True
#         news_subscription - булево поле обозначающее включение
#     или отключение подписки на новостную рассылку по дефолту False
#     """
#
#     class Meta:
#         verbose_name = 'Пользователь'
#         verbose_name_plural = 'Пользователи'
#
#     user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь")
#     user_response = models.BooleanField(default=True, verbose_name="Уведомление об откликах")
#     news_subscription = models.BooleanField(default=False, verbose_name="Новостная рассылка")
#
#     def __str__(self):
#         return f'{self.user}'


class Image(models.Model):
    """
        Модель изображения, содержащее поле:

        file - поле изображения
    """

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'

    file = models.ImageField(upload_to='board/files/images/', verbose_name="Изображение")



class Video(models.Model):
    """
        Модель видеороликов хранящее информацию о ссылках на ролики,
    которые будут напрямую запускаться на сайте. Содержит поля:

        url - поле хранящее ссылку на ролик
    """

    class Meta:
        verbose_name = 'Видео'
        verbose_name_plural = 'Видео'

    url = EmbedVideoField(verbose_name="Ссылка")


class Post(models.Model):
    """
        Модель поста, содержащее поля:

        title - текстовое поле для заголовка, максимум 200 символов
        text - текстовое поле для основного текста поста
        image - ManyToManyField связывающее Post и Image модели через PostImage модель
        video - ManyToManyField связывающее Post и Video модели через PostVideo модель
        author - связывающее поле с моделью Member
        category - текстовое поле для выбора категории поста
        time_in - поле для отслеживания времени создания поста
    """

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    title = models.CharField(max_length=200, verbose_name="Заголовок")
    text = models.TextField(verbose_name="Текст")
    image = models.ManyToManyField(Image, through='PostImage', verbose_name="Изображения")
    video = models.ManyToManyField(Video, through='PostVideo', verbose_name="Видео")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")
    category = models.CharField(max_length=2, choices=CATEGORY_CHOICE, verbose_name="Категория")
    time_in = models.DateTimeField(auto_now_add=True)

    def show_category(self):
        """
            Выводит название категории, а не его ключ
        """
        for category in CATEGORY_CHOICE:
            if self.category == category[0]:
                return category[1]

    def __str__(self):
        return f'{self.title}'


class PostVideo(models.Model):
    """
        Модель связывающая модели Post и Video для множественного
    добавления видео к посту, содержит поля:

        post - поле связанное с моделью Post
        video - поле связанное с моделью Video
    """

    class Meta:
        verbose_name = 'Пост-Видео'

    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name="Пост")
    video = models.ForeignKey(Video, on_delete=models.CASCADE, verbose_name="Видео")

    def __str__(self):
        return f'{self.post}: {self.video}'


class PostImage(models.Model):
    """
        Модель связывающая модели Post и Image для множественного
    добавления картинок к посту, содержит поля:

        post - поле связанное с моделью Post
        image - поле связанное с моделью Image
    """

    class Meta:
        verbose_name = 'Пост-Изображение'

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        verbose_name="Пост",
        help_text="Первое фото будет выбрано в качестве превью",
    )
    image = models.ForeignKey(Image, on_delete=models.CASCADE, verbose_name="Изображение")

    def __str__(self):
        return f'{self.post}: {self.image}'


class Comment(models.Model):
    """
        Модель отклика, содержащее поля:

        post - связывающее поле с моделью Post
        author - связывающее поле с моделью Member
        text - текстовое поле для комментария
        time_in - дата создания отклика
        confirmed - принял ли автор отклик, т.е. виден ли он остальным
    """

    class Meta:
        verbose_name = 'Отклик'
        verbose_name_plural = 'Отклики'

    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name="Пост")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")
    text = models.TextField(verbose_name="Текст")
    time_in = models.DateTimeField(auto_now_add=True)
    confirmed = models.BooleanField(default=False, verbose_name="Подтвержденный отклик")

    def __str__(self):
        return f'{self.text}'


class OneTimeCode(models.Model):
    """
        Модель создания для одноразового кода при регистрации, содержит поля:

        code - текстовое поле, которое хранит код до момента его активации
    или до истечения его срока
        user - поле связанное с моделью User для привязки кода к определенному
    пользователю
    """

    code = models.IntegerField(unique=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    time_in = models.DateTimeField(auto_now_add=True)

    def generate_code(self):
        """
            Функция генерирующая одноразовый код
        """

        self.code = random.randrange(100000, 999999)
        self.save()

    def __str__(self):
        return f'{self.code}'

