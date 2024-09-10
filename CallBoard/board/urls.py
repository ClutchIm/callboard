from django.urls import path

from .views import image, video, PostListView, PostDetailView

urlpatterns = [
    path('image/<int:image_id>', image, name='image'),
    path('video/', video, name='video'),
    path('post/', PostListView.as_view(), name='PostList'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='PostDetail'),
]
