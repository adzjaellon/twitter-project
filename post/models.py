from django.db import models
from django.conf import settings


class Post:
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, blank=True)
    bio = models.TextField(default='...', max_length=333)
    avatar = models.ImageField()

    def __str__(self):
        return self.author.username

    class Meta:
        ordering = ('-created', )

    def save(self, *args, **kwargs):
        self.slug = self.user.username + str(self.id)
        return super().save(*args, **kwargs)
