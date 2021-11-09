from .models import Post
from django.db.models import Count


def tags(request):
    return {
        'common_tags': Post.tags.values('name').annotate(count=Count('name')).order_by('-count')[:5]
    }


def latest_posts(request):
    return {
        'latest_posts': Post.objects.exclude(followers_only=True).order_by('-created')[:3]
    }
