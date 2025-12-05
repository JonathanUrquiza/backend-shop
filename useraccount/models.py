from django.db import models


class User(models.Model):
    """Modelo que representa un usuario."""
    user_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=16)
    lastname = models.CharField(max_length=80)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=32)
    create_time = models.DateTimeField(blank=True, null=True)
    role_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False  # Las tablas ya existen en la BD
        db_table = 'user'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return f"{self.name} {self.lastname}"


class Role(models.Model):
    """Modelo que representa un rol de usuario."""
    role_id = models.AutoField(primary_key=True)
    role_name = models.CharField(max_length=60)

    class Meta:
        managed = False  # Las tablas ya existen en la BD
        db_table = 'role'
        verbose_name = 'Rol'
        verbose_name_plural = 'Roles'

    def __str__(self):
        return self.role_name
