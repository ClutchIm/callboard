from multiprocessing.reduction import register

from django.contrib import admin


from .models import (
    Member, Image, Video, Post, Comment
)


class PostAdmin(admin.ModelAdmin):
    model = Post
    list_display = ('id', 'title', 'text', 'image', 'author', 'category',)


class ImageAdmin(admin.ModelAdmin):
    model = Image
    list_display = ('id', 'name', 'file',)


# Register your models here.

admin.site.register(Post, PostAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Video)
admin.site.register(Comment)
admin.site.register(Member)


