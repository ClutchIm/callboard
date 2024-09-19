from django.urls import path, include

from .views import image, video, PostListView, PostDetailView, logout_view, register, verify, RegisterView

urlpatterns = [
    path('image/<int:image_id>', image, name='image'),
    path('video/', video, name='video'),
    path('post/', PostListView.as_view(), name='PostList'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='PostDetail'),
    # path('register/', RegisterView.as_view(), name='register'),
    path('user/logout/', logout_view, name='logout'),
    path('user/', include('django.contrib.auth.urls')),
    path('register/', register, name='register'),
    path('verify_otp/<int:user_id>/', verify, name='verify_otp'),
]
