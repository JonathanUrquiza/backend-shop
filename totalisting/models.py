from django.db import models


class Category(models.Model):
    """Modelo que representa una categoría de productos."""
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=100)
    category_description = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False  # Las tablas ya existen en la BD
        db_table = 'category'
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'

    def __str__(self):
        return self.category_name


class Licence(models.Model):
    """Modelo que representa una licencia de producto."""
    licence_id = models.AutoField(primary_key=True)
    licence_name = models.CharField(max_length=45)
    licence_description = models.CharField(max_length=255)
    licence_image = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False  # Las tablas ya existen en la BD
        db_table = 'licence'
        verbose_name = 'Licencia'
        verbose_name_plural = 'Licencias'

    def __str__(self):
        return self.licence_name


class Product(models.Model):
    """Modelo que representa un producto."""
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=60)
    product_description = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    discount = models.IntegerField(blank=True, null=True)
    sku = models.CharField(unique=True, max_length=30)
    dues = models.IntegerField(blank=True, null=True)
    created_by = models.IntegerField()
    image_front = models.CharField(max_length=200)
    image_back = models.CharField(max_length=200)
    create_time = models.DateTimeField(blank=True, null=True)
    licence = models.ForeignKey(Licence, on_delete=models.DO_NOTHING, db_column='licence_id')
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, db_column='category_id')

    class Meta:
        managed = False  # Las tablas ya existen en la BD
        db_table = 'product'
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'

    def __str__(self):
        return self.product_name




"""
================================================================================
MÓDULO: totalisting/models.py
================================================================================

DESCRIPCIÓN:
Este módulo define los modelos de Django que representan las tablas existentes
en la base de datos MySQL en la nube. Los modelos actúan como una capa de
abstracción ORM (Object-Relational Mapping) que permite interactuar con las
tablas de la base de datos usando objetos Python en lugar de consultas SQL
directas.

IMPORTANTE:
- Todos los modelos tienen `managed = False` porque las tablas ya existen en
  la base de datos. Django NO creará, modificará ni eliminará estas tablas
  automáticamente mediante migraciones.
- Los nombres de las tablas se especifican mediante `db_table` para mantener
  la compatibilidad con la estructura existente en la base de datos.

MODELOS INCLUIDOS:

1. Category (Categoría)
   - Representa las categorías de productos disponibles en el sistema.
   - Campos: category_id, category_name, category_description

2. Licence (Licencia)
   - Representa las licencias asociadas a los productos (ej: Marvel, DC, etc.).
   - Campos: licence_id, licence_name, licence_description, licence_image

3. Product (Producto)
   - Representa los productos del catálogo de la tienda.
   - Relaciones: ForeignKey con Category y Licence
   - Campos: product_id, product_name, product_description, price, stock,
     discount, sku, dues, created_by, image_front, image_back, create_time

4. Role (Rol)
   - Representa los roles de usuario en el sistema.
   - Campos: role_id, role_name

USO:
Para usar estos modelos en tus vistas o scripts, importa los modelos necesarios:

    from totalisting.models import Product, Category, Licence, Role
    
    # Ejemplo: Obtener todos los productos
    productos = Product.objects.all()
    
    # Ejemplo: Filtrar productos por categoría
    productos_categoria = Product.objects.filter(category__category_name='Figuras')

CONFIGURACIÓN:
- Base de datos: MySQL en la nube (mysql-funkotest.alwaysdata.net)
- Nombre de la base de datos: funkotest_funkos
- Configuración de conexión: Ecommerce/settings.py

================================================================================
"""
