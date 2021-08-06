from django import forms
from .models import Comment, Post


class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body', )
        widgets = {
            'body': forms.Textarea(attrs={'name': 'usercomment', 'id': 'usercomment', 'class': 'form-control'})
        }


class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('body', 'tags', 'picture', 'followers_only')

