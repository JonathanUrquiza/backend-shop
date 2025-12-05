# Importar el módulo models de Django para definir modelos de base de datos
from django.db import models


class User(models.Model):
    """
    Modelo que representa un usuario del sistema.
    
    Este modelo mapea la tabla 'user' de la base de datos y permite
    interactuar con los usuarios usando el ORM de Django.
    
    Los usuarios pueden tener diferentes roles (admin, vendedor, comprador, mixto)
    que determinan sus permisos en el sistema.
    """
    # Campo de clave primaria auto-incremental (ID único del usuario)
    user_id = models.AutoField(primary_key=True)
    
    # Nombre del usuario (máximo 16 caracteres, obligatorio)
    name = models.CharField(max_length=16)
    
    # Apellido del usuario (máximo 80 caracteres, obligatorio)
    lastname = models.CharField(max_length=80)
    
    # Email del usuario (máximo 255 caracteres, obligatorio, debe ser único)
    # Se usa como identificador para login
    email = models.CharField(max_length=255)
    
    # Contraseña del usuario (máximo 32 caracteres, obligatorio)
    # NOTA: En producción, esto debería estar hasheado, no en texto plano
    password = models.CharField(max_length=32)
    
    # Fecha y hora de registro del usuario (opcional)
    create_time = models.DateTimeField(blank=True, null=True)
    
    # ID del rol asignado al usuario (opcional)
    # Referencia al modelo Role que define los permisos del usuario
    # None significa que el usuario no tiene rol asignado
    role_id = models.IntegerField(blank=True, null=True)

    class Meta:
        # Indicar a Django que NO gestione esta tabla (ya existe en la BD)
        managed = False
        # Nombre de la tabla en la base de datos
        db_table = 'user'
        # Nombre legible en singular para el admin de Django
        verbose_name = 'Usuario'
        # Nombre legible en plural para el admin de Django
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        """
        Retorna una representación en string del objeto User.
        
        Se usa cuando se imprime el objeto o se muestra en el admin de Django.
        
        Returns:
            str: Nombre completo del usuario (nombre + apellido)
        """
        return f"{self.name} {self.lastname}"


class Role(models.Model):
    """
    Modelo que representa un rol de usuario en el sistema.
    
    Este modelo mapea la tabla 'role' de la base de datos y permite
    interactuar con los roles usando el ORM de Django.
    
    Los roles definen los permisos y capacidades de los usuarios:
    - admin: Acceso completo al sistema
    - vendedor: Puede gestionar productos
    - comprador: Puede comprar productos
    - mixto: Puede hacer funciones de vendedor y comprador
    """
    # Campo de clave primaria auto-incremental (ID único del rol)
    role_id = models.AutoField(primary_key=True)
    
    # Nombre del rol (máximo 60 caracteres, obligatorio)
    # Ejemplos: "admin", "vendedor", "comprador", "mixto"
    role_name = models.CharField(max_length=60)

    class Meta:
        # Indicar a Django que NO gestione esta tabla (ya existe en la BD)
        managed = False
        # Nombre de la tabla en la base de datos
        db_table = 'role'
        # Nombre legible en singular para el admin de Django
        verbose_name = 'Rol'
        # Nombre legible en plural para el admin de Django
        verbose_name_plural = 'Roles'

    def __str__(self):
        """
        Retorna una representación en string del objeto Role.
        
        Se usa cuando se imprime el objeto o se muestra en el admin de Django.
        
        Returns:
            str: Nombre del rol
        """
        return self.role_name
