from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile
from django.utils.text import slugify
from django.utils.crypto import get_random_string


@receiver(post_save, sender=User)
def post_save_create_profile(sender, instance, created, **kwargs):
    if created:
        slug = slugify(instance.id) + slugify(get_random_string(16))
        Profile.objects.create(user=instance, slug=slug)
