from django.db import models
from django.conf import settings


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    avatar = models.ImageField(default='default-avatar.png', upload_to='profile_pictures/')
    following = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='following', blank=True)
    slug = models.SlugField(unique=True, blank=True)
    bio = models.TextField(default='...', max_length=333)
    email = models.EmailField(blank=True)

    def __str__(self):
        return self.user.username

    class Meta:
        ordering = ('-created', )

    def save(self, *args, **kwargs):
        slugs = [profile.slug for profile in Profile.objects.all()]
        self.slug = self.user.username + str(self.user.id)
        while self.slug in slugs:
            self.slug += str(self.user.id)
        return super().save(*args, **kwargs)
