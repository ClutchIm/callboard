from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from .models import Post, Member


User = get_user_model()

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title',
            'text',
        ]

class UserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User

    email = forms.EmailField(required=True)




