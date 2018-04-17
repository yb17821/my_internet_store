from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib.auth import get_user_model
User = get_user_model()

@receiver(post_save, sender=User)
def create_user(sender, instance=None, created=False, **kwargs):
    if created:
        password = instance.password
        instance.set_password(password)
        instance.save()

        # 可以在这里为新建的用户设置token，但是由于使用了jwt验证，所以，这个不需要
        # Token.objects.create(user=instance)
