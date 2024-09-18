from django import forms

from .models import Post, Member


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title',
            'text',
        ]

