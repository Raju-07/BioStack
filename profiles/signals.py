from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Subscription

User = get_user_model()

@receiver(post_save, sender=User)
def create_user_subscription(sender, instance, created, **kwargs):
    if created:
        Subscription.objects.create(user=instance,plan_type='FREE')

@receiver(post_save, sender=User)
def save_user_subscription(sender, instance, **kwargs):
    if not hasattr(instance, 'subscription'):
        Subscription.objects.create(user=instance)
    instance.subscription.save()