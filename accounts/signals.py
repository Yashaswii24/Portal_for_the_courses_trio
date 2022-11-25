from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import user, Profile
""" Used for autogeneration of profile data when user data is generated
"""
@receiver(post_save, sender=user)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user_details=instance)