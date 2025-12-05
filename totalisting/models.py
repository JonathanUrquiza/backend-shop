# Importar el módulo models de Django para definir modelos de base de datos
from django.db import models


class Category(models.Model):
    """
    Modelo que representa una categoría de productos.
    
    Este modelo mapea la tabla 'category' de la base de datos y permite
    interactuar con las categorías de productos usando el ORM de Django.
    
    Ejemplos de categorías: "Figuras", "Llaveros", "Remeras", etc.
    """
    # Campo de clave primaria auto-incremental (ID único de la categoría)
    category_id = models.AutoField(primary_key=True)
    
    # Nombre de la categoría (máximo 100 caracteres, obligatorio)
    category_name = models.CharField(max_length=100)
    
    # Descripción de la categoría (máximo 255 caracteres, opcional)
    category_description = models.CharField(max_length=255, blank=True, null=True)
    
    # Ruta de la imagen asociada a la categoría (opcional)
    # Almacena la ruta relativa de la imagen en el sistema de archivos
    image_category = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        # Indicar a Django que NO gestione esta tabla (ya existe en la BD)
        # Django no creará, modificará ni eliminará esta tabla mediante migraciones
        managed = False
        # Nombre de la tabla en la base de datos
        db_table = 'category'
        # Nombre legible en singular para el admin de Django
        verbose_name = 'Categoría'
        # Nombre legible en plural para el admin de Django
        verbose_name_plural = 'Categorías'

    def __str__(self):
        """
        Retorna una representación en string del objeto Category.
        
        Se usa cuando se imprime el objeto o se muestra en el admin de Django.
        
        Returns:
            str: Nombre de la categoría
        """
        return self.category_name


class Licence(models.Model):
    """
    Modelo que representa una licencia de producto.
    
    Este modelo mapea la tabla 'licence' de la base de datos y permite
    interactuar con las licencias de productos usando el ORM de Django.
    
    Las licencias representan las marcas o franquicias asociadas a los productos
    (ej: "Star Wars", "Pokemon", "Harry Potter", "Marvel", etc.).
    """
    # Campo de clave primaria auto-incremental (ID único de la licencia)
    licence_id = models.AutoField(primary_key=True)
    
    # Nombre de la licencia (máximo 45 caracteres, obligatorio)
    # Ejemplos: "Star Wars", "Pokemon", "Harry Potter"
    licence_name = models.CharField(max_length=45)
    
    # Descripción de la licencia (máximo 255 caracteres, obligatorio)
    licence_description = models.CharField(max_length=255)
    
    # Ruta de la imagen asociada a la licencia (opcional)
    # Almacena la ruta relativa de la imagen en el sistema de archivos
    licence_image = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        # Indicar a Django que NO gestione esta tabla (ya existe en la BD)
        managed = False
        # Nombre de la tabla en la base de datos
        db_table = 'licence'
        # Nombre legible en singular para el admin de Django
        verbose_name = 'Licencia'
        # Nombre legible en plural para el admin de Django
        verbose_name_plural = 'Licencias'

    def __str__(self):
        """
        Retorna una representación en string del objeto Licence.
        
        Se usa cuando se imprime el objeto o se muestra en el admin de Django.
        
        Returns:
            str: Nombre de la licencia
        """
        return self.licence_name


class Product(models.Model):
    """
    Modelo que representa un producto del catálogo de la tienda.
    
    Este modelo mapea la tabla 'product' de la base de datos y permite
    interactuar con los productos usando el ORM de Django.
    
    Un producto tiene relaciones con Category (categoría) y Licence (licencia),
    y puede tener múltiples imágenes (frontal, reverso y adicionales).
    """
    # Campo de clave primaria auto-incremental (ID único del producto)
    product_id = models.AutoField(primary_key=True)
    
    # Nombre del producto (máximo 60 caracteres, obligatorio)
    # Ejemplo: "Baby Yoda Blueball", "Pikachu Smiley"
    product_name = models.CharField(max_length=60)
    
    # Descripción del producto (máximo 255 caracteres, obligatorio)
    product_description = models.CharField(max_length=255)
    
    # Precio del producto (decimal con 10 dígitos totales, 2 decimales)
    # Ejemplo: 5200.99
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Cantidad disponible en stock (número entero, obligatorio)
    stock = models.IntegerField()
    
    # Descuento aplicado al producto en porcentaje (opcional)
    # Ejemplo: 10 significa 10% de descuento
    discount = models.IntegerField(blank=True, null=True)
    
    # SKU (Stock Keeping Unit) - código único de identificación del producto
    # Debe ser único en toda la base de datos (máximo 30 caracteres)
    # Ejemplo: "STW001001", "PKM001001"
    sku = models.CharField(unique=True, max_length=30)
    
    # Número de cuotas disponibles para pagar el producto (opcional)
    # Ejemplo: 3, 6, 12 (representa cuotas sin interés)
    dues = models.IntegerField(blank=True, null=True)
    
    # ID del usuario que creó el producto (número entero, obligatorio)
    # Referencia al usuario que agregó el producto al sistema
    created_by = models.IntegerField()
    
    # Ruta de la imagen frontal del producto (máximo 200 caracteres, obligatorio)
    # Esta imagen se muestra en la lista de productos
    # Ejemplo: "/star-wars/baby-yoda-1.webp"
    image_front = models.CharField(max_length=200)
    
    # Ruta de la imagen reverso del producto (máximo 200 caracteres, obligatorio)
    # Esta imagen muestra el reverso del empaque del producto
    # Ejemplo: "/star-wars/baby-yoda-box.webp"
    image_back = models.CharField(max_length=200)
    
    # Imágenes adicionales almacenadas como JSON string (opcional)
    # Contiene un array JSON con rutas de imágenes adicionales para la vista de detalle
    # Ejemplo: '["/star-wars/baby-yoda-2.webp", "/star-wars/baby-yoda-3.webp"]'
    additional_images = models.TextField(blank=True, null=True)
    
    # Fecha y hora de creación del producto (opcional)
    create_time = models.DateTimeField(blank=True, null=True)
    
    # Relación ForeignKey con el modelo Licence (licencia del producto)
    # on_delete=models.DO_NOTHING: No hacer nada si se elimina la licencia
    # db_column='licence_id': Nombre de la columna en la BD
    licence = models.ForeignKey(Licence, on_delete=models.DO_NOTHING, db_column='licence_id')
    
    # Relación ForeignKey con el modelo Category (categoría del producto)
    # on_delete=models.DO_NOTHING: No hacer nada si se elimina la categoría
    # db_column='category_id': Nombre de la columna en la BD
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, db_column='category_id')

    class Meta:
        # Indicar a Django que NO gestione esta tabla (ya existe en la BD)
        managed = False
        # Nombre de la tabla en la base de datos
        db_table = 'product'
        # Nombre legible en singular para el admin de Django
        verbose_name = 'Producto'
        # Nombre legible en plural para el admin de Django
        verbose_name_plural = 'Productos'

    def __str__(self):
        """
        Retorna una representación en string del objeto Product.
        
        Se usa cuando se imprime el objeto o se muestra en el admin de Django.
        
        Returns:
            str: Nombre del producto
        """
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
