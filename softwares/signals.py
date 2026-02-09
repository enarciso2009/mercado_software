from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Perfil

@receiver(post_save, sender=User)
def criar_profile(sender, instance, created, **kwargs):
    if created:
        if instance.is_superuser:
            Perfil.objects.create(user=instance, tipo_usuario='VENDEDOR')
        else:
            Perfil.objects.create(user=instance, tipo_usuario="COMPRADOR")




