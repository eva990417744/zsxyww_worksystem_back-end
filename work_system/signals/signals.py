from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from work_system.models import Personal





@receiver(post_save, sender=User)
def person(sender, instance, created, **kwargs):
    if created:
        Personal.objects.create(user=instance)
    instance.personal.save()
