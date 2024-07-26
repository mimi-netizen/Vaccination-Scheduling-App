from django.dispatch import receiver
from django.db import models
from django.contrib.auth import get_user_model
import os

User = get_user_model()

@receiver(models.signals.pre_save, sender=User)
def auto_delete_file_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False
    
    try:
        old_photo = User.objects.get(pk=instance.pk).photo
    except User.DoesNotExist:
        return False
    
    new_photo = instance.photo

    if bool(old_photo) and new_photo != old_photo:
        if os.path.isfile(old_photo.path):
            os.remove(old_photo.path)