from django.db import models
from django.conf import settings
from user_profile.models import Profile
from django.utils.text import slugify
from taggit.managers import TaggableManager
from django.shortcuts import reverse


class Post(models.Model):
    body = models.TextField(max_length=700)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, blank=True)
    picture = models.ImageField(upload_to='post_pictures/')

    tags = TaggableManager()

    @property
    def comments(self):
        return self.comment_set.all().order_by('-created')

    def get_tags(self):
        return self.tags.all()

    def get_common_tags(self):
        return Post.tags.most_common()[:5]

    def get_comment_number(self):
        return self.comment_set.all().count()

    def __str__(self):
        return f'Post: {self.author.user.username}-{self.created}-{self.body[:10]}'

    def save(self, *args, **kwargs):
        self.slug = str(slugify(self.created)) + str(self.author.id)
        return super().save(*args, **kwargs)

    class Meta:
        ordering = ('-created', )


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    body = models.TextField()
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment: {self.author.user.username} | {self.created}'
