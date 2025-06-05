from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class UsuarioPersonalizado(AbstractUser):
    # Campos personalizados
    fecha_nacimiento = models.DateField(null=True, blank=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    # Usar BinaryField en lugar de ImageField para guardar como BLOB
    profile_picture = models.BinaryField(blank=True, null=True)
    profile_picture_name = models.CharField(max_length=100, blank=True, null=True)  # Para guardar el nombre del archivo
    profile_picture_type = models.CharField(max_length=30, blank=True, null=True)   # Para guardar el tipo MIME
    
    # Arreglar las relaciones para evitar colisiones con el modelo User predeterminado
    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='usuariopersonalizado_set'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='usuariopersonalizado_set'
    )
    
    def __str__(self):
        return self.username