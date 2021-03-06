from django.contrib import admin
from .models import Post, Comment, LikeUnlike


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['body', 'author', 'created']
    list_filter = ['followers_only', 'created', 'author']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'created']
    list_filter = ['created', 'author']


@admin.register(LikeUnlike)
class CommentAdmin(admin.ModelAdmin):
    pass
