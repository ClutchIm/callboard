from django import template

from board.models import Image, PostImage, Post, PostVideo


register = template.Library()


@register.filter
def preview(value: Post) -> Image:
    """
        Принимает объект модели Post и возвращает первую картинку в этой модели
    """

    img = PostImage.objects.filter(post=value).first()
    return img.image.file.url


@register.filter
def image_check(value: Post) -> bool:
    """
        Принимает объект модели Post и проверяет есть ли в нем прикрепленные картинки
    """


    if PostImage.objects.filter(post=value.id).first():
        return True
    else:
        return False


@register.filter
def video_check(value: Post) -> bool:
    """
        Принимает объект модели Post и проверяет есть ли в нем прикрепленные видео
    """

    if PostVideo.objects.filter(post=value.id).first():
        return True
    else:
        return False


@register.filter
def get_image(value: Post) -> list[PostImage]:
    """
        Принимает объект модели Post, обрабатывая, возвращает список всех связанных изображений
    """

    return PostImage.objects.filter(post=value.id).all()


@register.filter
def get_video(value: Post) -> list[PostVideo]:
    """
        Принимает объект модели Post, обрабатывая, возвращает список всех связанных видео
    """

    return PostVideo.objects.filter(post=value.id).all()

