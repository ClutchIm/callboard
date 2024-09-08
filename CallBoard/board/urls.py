from django.urls import path

from .views import image


urlpatterns = [
    path('image/<int:image_id>', image, name='image'),
]
