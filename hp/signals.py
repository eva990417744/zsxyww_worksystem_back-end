from django.db.models.signals import post_save
from django.dispatch import receiver
from work_system.models import Personal
from django.contrib.auth.models import User
from .models import *


@receiver(post_save, sender=User)
def createHP(sender, instance, created, **kwargs):
    if created:
        HP.objects.create(user=instance)


@receiver(post_save, sender=Buff)
def increaseHP(sender, instance, created, **kwargs):
    if created:
        q = instance.key
        q.value += 5
        q.save()
        super(Buff, instance).save()


@receiver(post_save, sender=DeBuff)
def decreaseHP(sender, instance, created, **kwargs):
    if created:
        q = instance.key
        if instance.debuff_reason in Summary.DeBuff_Lv1:
            instance.hp_decrease = 10
            q.value -= 10
        elif instance.debuff_reason in Summary.DeBuff_Lv2:
            instance.hp_decrease = 20
            q.value -= 20
        elif instance.debuff_reason in Summary.DeBuff_Lv3:
            instance.hp_decrease = 30
            q.value -= 30
        q.save()
        super(DeBuff, instance).save()

