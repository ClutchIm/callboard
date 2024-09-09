from multiprocessing.reduction import register

from django.contrib import admin


from .models import (
    Member, Image, Video, Post, Comment, PostVideo, PostImage
)


class VideoInLine(admin.TabularInline):
    model = PostVideo
    extra = 1
    max_num = 3


class ImageInLine(admin.TabularInline):
    model = PostImage
    extra = 1
    max_num = 10


class PostAdmin(admin.ModelAdmin):
    model = Post
    list_display = ('id', 'title', 'text', 'author', 'category',)
    inlines = [VideoInLine, ImageInLine]

# Register your models here.

admin.site.register(Post, PostAdmin)
admin.site.register(Image)
admin.site.register(Video)
admin.site.register(Comment)
admin.site.register(Member)


