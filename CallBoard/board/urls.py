from django.urls import path, include

from .views import (
    image, video, PostListView, PostDetailView, logout_view, register, verify, PersonalOfficeView,
    PostCreateView, PostUpdateView, PostDeleteView, delete_image, delete_video, repeat_verify
)

urlpatterns = [
    path('image/<int:image_id>', image, name='image'),
    path('video/', video, name='video'),
    path('post/', PostListView.as_view(), name='PostList'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='PostDetail'),
    path('user/logout/', logout_view, name='logout'),
    path('user/', include('django.contrib.auth.urls')),
    path('register/', register, name='register'),
    path('verify_otp/<int:user_id>/', verify, name='verify_otp'),
    path('verify_otp/', repeat_verify, name='repeat_verify'),
    path('personal/', PersonalOfficeView.as_view(), name='personal'),
    path('post/create/', PostCreateView.as_view(), name='post_create'),
    path('post/update/<int:pk>/', PostUpdateView.as_view(), name='post_update'),
    path('post/delete/<int:pk>/', PostDeleteView.as_view(), name='post_delete'),
    path('delete-image/<int:pk>/', delete_image, name='delete_image'),
    path('delete-video/<int:pk>/', delete_video, name='delete_video'),
]
