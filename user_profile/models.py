from django.db import models
from django.conf import settings
from post.models import LikeUnlike


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    avatar = models.ImageField(default='default-avatar.png', upload_to='profile_pictures/')
    following = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='following', blank=True)
    slug = models.SlugField(unique=True, blank=True)
    bio = models.TextField(default='...', max_length=333)
    email = models.EmailField(blank=True)

    @property
    def get_posts_number(self):
        return self.posts.all().count()

    @property
    def get_latest_likes(self):
        return LikeUnlike.objects.filter(profile=self).order_by('-created')[:4]

    def __str__(self):
        return self.user.username

    class Meta:
        ordering = ('-created', )

