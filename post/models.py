from django.db import models
from django.conf import settings
from user_profile.models import Profile


class Post(models.Model):
    body = models.TextField(max_length=700)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, blank=True)
    picture = models.ImageField(blank=True, upload_to='post_pictures/')
    email = models.EmailField()

    def __str__(self):
        return f'Post: {self.author.username}-{self.created}'

    class Meta:
        ordering = ('-created', )

    def save(self, *args, **kwargs):
        slugs = [post.slug for post in Post.objects.all()]
        self.slug = str(self.created) + str(self.user.id)
        while self.slug in slugs:
            self.slug += str(self.user.id)
        return super().save(*args, **kwargs)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    body = models.TextField()
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment: {self.author.username} | {self.created}'