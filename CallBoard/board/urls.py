from django.urls import path, include

from .views import image, video, PostListView, PostDetailView

urlpatterns = [
    path('image/<int:image_id>', image, name='image'),
    path('video/', video, name='video'),
    path('post/', PostListView.as_view(), name='PostList'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='PostDetail'),
    # path('register/', RegisterView.as_view(), name='register'),
    path('', include('django.contrib.auth.urls')),
]
