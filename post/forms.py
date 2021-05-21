from django.forms import ModelForm, Textarea
from .models import Comment, Post


class CommentCreateForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('body', )
        widgets = {
            'body': Textarea(attrs={'name': 'usercomment', 'id': 'usercomment', 'class': 'form-control'})
        }


class PostCreateForm(ModelForm):
    class Meta:
        model = Post
        fields = ('body', 'tags', 'picture')
