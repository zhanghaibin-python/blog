from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    当 User 对象被创建时， 自动创建对应的 UserProfile
    """
    if created:
        UserProfile.objects.create(
            user=instance,
            nickname=instance.username
        )


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    保存 User 时同步保存 Profile (防御性编程)
    """
    # 检查是否有关联的 profile，避免某些极端情况
    if hasattr(instance, 'profile'):
        instance.profile.save()