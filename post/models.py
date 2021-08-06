from django.db import models
from django.conf import settings
from taggit.managers import TaggableManager


class Post(models.Model):
    body = models.TextField(max_length=700)
    author = models.ForeignKey('user_profile.Profile', on_delete=models.CASCADE, related_name='posts')
    created = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, blank=True)
    picture = models.ImageField(upload_to='post_pictures/')
    tags = TaggableManager()
    followers_only = models.BooleanField(default=False)
    likes = models.ManyToManyField('user_profile.Profile', related_name='likes', blank=True)

    @property
    def comments(self):
        return self.comment_set.all().order_by('-created')

    @property
    def total_likes(self):
        return self.likes.all().count()

    def get_tags(self):
        return self.tags.all()

    def get_common_tags(self):
        return Post.tags.most_common()[:5]

    def get_comment_number(self):
        return self.comment_set.all().count()

    def __str__(self):
        return f'Post: {self.author.user.username}-{self.created}-{self.body[:10]}'

    class Meta:
        ordering = ('-created', )


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    body = models.TextField()
    author = models.ForeignKey('user_profile.Profile', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment: {self.author.user.username} | {self.created}'


CHOICES = (
    ('Like', 'Like'),
    ('Unlike', 'Unlike')
)


class LikeUnlike(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey('user_profile.Profile', on_delete=models.CASCADE)
    status = models.CharField(choices=CHOICES, max_length=6, default='Unlike')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.profile}-{self.post}-{self.status}'
