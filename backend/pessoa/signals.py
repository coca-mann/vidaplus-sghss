from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from backend.pessoa.models.paciente import Paciente


@receiver(post_save, sender=Paciente)
def create_user_for_paciente(sender, instance, created, **kwargs):
    if created:
        if not User.objects.filter(username=instance.cpf).exists():
            user = User.objects.create_user(
                username=instance.cpf,
                email=instance.email,
                password='123456'
            )
        
        instance.idUsuario = user
        instance.save()
