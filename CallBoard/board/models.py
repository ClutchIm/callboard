from django.contrib.auth.models import User
from django.db import models

import random


class Member(models.Model):
    """
        Модель пользователя, содержащее поля:

        user - поле связанное напрямую с моделью User
        user_response - булево поле обозначающее согласие
    на отправку уведомлений на e-mail об ответе на отклик
    по дефолту True
        news_subscription - булево поле обозначающее включение
    или отключение подписки на новостную рассылку по дефолту False
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_response = models.BooleanField(default=True)
    news_subscription = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user}'


class Image(models.Model):
    """
        Модель изображения, содержащее поле:

        name - текстовое поле для имени картинки
        image - поле изображения
    """

    name = models.CharField(max_length=120)
    image = models.ImageField(upload_to='board/files/images/')

    def __str__(self):
        return self.name


class Post(models.Model):
    """
        Модель поста, содержащее поля:

        title - текстовое поле для заголовка, максимум 200 символов
        text - текстовое поле для основного текста поста
        author - связывающее поле с моделью Member
        category -
        time_in - поле для отслеживания времени создания поста
    """

    CATEGORY_CHOICE = [
        ("TA", "Танки"),
        ("HE", "Хилы"),
        ("DD", "ДД"),
        ("TR", "Торговцы"),
        ("GM", "Гильдмастеры"),
        ("QG", "Квестгиверы"),
        ("BS", "Кузнецы"),
        ("SK", "Кожевники"),
        ("AL", "Зельевары"),
        ("SM", "Мастера заклинаний"),
    ]

    title = models.CharField(max_length=200)
    text = models.TextField()
    image = models.ForeignKey(Image, on_delete=models.CASCADE, blank=True)
    author = models.ForeignKey(Member, on_delete=models.CASCADE)
    category = models.CharField(max_length=2, choices=CATEGORY_CHOICE)
    time_in = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title}'


class Comment(models.Model):
    """
        Модель отклика, содержащее поля:

        post - связывающее поле с моделью Post
        author - связывающее поле с моделью Member
        text - текстовое поле для комментария
        time_in - дата создания отклика
        confirmed - принял ли автор отклик, т.е. виден ли он остальным
    """

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(Member, on_delete=models.CASCADE)
    text = models.TextField()
    time_in = models.DateTimeField(auto_now_add=True)
    confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.text}'


class OneTimeCode(models.Model):
    """
        Модель создания одноразового кода для регистрации, содержит поля:

        code - текстовое поле, которое хранит код до момента его активации
    или до истечения его срока

        generate_code() - функция генерирующая одноразовый код
    """

    code = models.IntegerField(unique=True, blank=True)

    def generate_code(self):
        self.code = random.randrange(100000, 999999)
        self.save()

    def __str__(self):
        return f'{self.code}'

