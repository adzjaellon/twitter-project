from django.forms import ModelForm
from .models import Comment, Post


class CommentCreateForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('body', )


class PostCreateForm(ModelForm):
    class Meta:
        model = Post
        fields = ('body', 'tags', 'picture')