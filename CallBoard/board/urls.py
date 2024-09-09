from django.urls import path

from .views import image, video


urlpatterns = [
    path('image/<int:image_id>', image, name='image'),
    path('video/', video, name='video'),
]
