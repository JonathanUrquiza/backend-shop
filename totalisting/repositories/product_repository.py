"""
Repositorio para el modelo Product.

Este módulo contiene la clase ProductRepository que abstrae todas las operaciones
de acceso a datos relacionadas con productos. Implementa el Repository Pattern
que separa la lógica de acceso a datos de la lógica de negocio.

El repositorio proporciona métodos para:
- Obtener productos (todos, por ID, por nombre, por SKU, filtrados)
- Crear productos
- Actualizar productos
- Eliminar productos
- Verificar existencia de SKU

Todas las consultas a la base de datos relacionadas con productos deben pasar
por este repositorio, no acceder directamente al modelo Product.
"""

# Importar tipos de Python para type hints
from typing import Optional, List
# Importar excepciones de Django para manejo de errores de base de datos
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
# Importar el modelo Product para trabajar con instancias
from ..models import Product


class ProductRepository:
    """
    Repositorio para productos.
    
    Esta clase encapsula todas las operaciones de acceso a datos relacionadas
    con productos. Proporciona una interfaz limpia y consistente para interactuar
    con la tabla 'product' de la base de datos.
    
    Todos los métodos son estáticos, lo que significa que no se necesita
    instanciar la clase para usarlos.
    """
    
    @staticmethod
    def get_all() -> List[Product]:
        """
        Obtiene todos los productos ordenados por nombre.
        
        Este método retorna todos los productos de la base de datos ordenados
        alfabéticamente por nombre. Es útil para listar todos los productos
        en el catálogo.
        
        Returns:
            List[Product]: Lista de todos los productos ordenados por nombre
                         Lista vacía si no hay productos
        
        Ejemplo:
            >>> products = ProductRepository.get_all()
            >>> len(products)
            13
        """
        # Obtener todos los productos usando el ORM de Django
        # .all() obtiene todos los registros
        # .order_by('product_name') ordena alfabéticamente por nombre
        # list() convierte el QuerySet a lista de Python
        return list(Product.objects.all().order_by('product_name'))
    
    @staticmethod
    def get_by_id(product_id: int) -> Optional[Product]:
        """
        Obtiene un producto por su ID.
        
        Este método busca un producto específico usando su ID único.
        Es el método más eficiente para obtener un producto cuando se conoce su ID.
        
        Args:
            product_id: ID único del producto a buscar (número entero)
            
        Returns:
            Optional[Product]: Instancia del Product si existe, None si no se encuentra
            
        Ejemplo:
            >>> product = ProductRepository.get_by_id(1)
            >>> if product:
            ...     print(product.product_name)
            'Baby Yoda Blueball'
        """
        try:
            # Usar .get() para obtener un único producto por ID
            # .get() lanza excepción si no encuentra o encuentra múltiples
            return Product.objects.get(product_id=product_id)
        except ObjectDoesNotExist:
            # Si el producto no existe, retornar None en lugar de lanzar excepción
            # Esto hace el código más robusto y fácil de manejar
            return None
    
    @staticmethod
    def get_by_name(product_name: str) -> Optional[Product]:
        """
        Obtiene un producto por su nombre.
        
        Este método busca un producto por su nombre exacto. Si hay múltiples
        productos con el mismo nombre, retorna None (el nombre debería ser único
        pero no está garantizado en la BD).
        
        Args:
            product_name: Nombre exacto del producto a buscar (string)
            
        Returns:
            Optional[Product]: Instancia del Product si existe y es único,
                             None si no se encuentra o hay múltiples resultados
            
        Ejemplo:
            >>> product = ProductRepository.get_by_name("Baby Yoda Blueball")
            >>> if product:
            ...     print(product.product_id)
            1
        """
        try:
            # Buscar producto por nombre exacto
            # .get() requiere coincidencia exacta del nombre
            return Product.objects.get(product_name=product_name)
        except ObjectDoesNotExist:
            # Si no se encuentra el producto, retornar None
            return None
        except MultipleObjectsReturned:
            # Si hay múltiples productos con el mismo nombre (no debería pasar),
            # retornar None en lugar de lanzar excepción
            return None
    
    @staticmethod
    def get_by_sku(sku: str) -> Optional[Product]:
        """
        Obtiene un producto por su SKU (Stock Keeping Unit).
        
        El SKU es un código único que identifica cada producto. Este método
        es útil para buscar productos cuando se conoce el SKU (ej: desde
        un código de barras o referencia externa).
        
        Args:
            sku: SKU del producto a buscar (string, ej: "STW001001")
            
        Returns:
            Optional[Product]: Instancia del Product si existe, None si no se encuentra
            
        Ejemplo:
            >>> product = ProductRepository.get_by_sku("STW001001")
            >>> if product:
            ...     print(product.product_name)
            'Baby Yoda Blueball'
        """
        try:
            # Buscar producto por SKU exacto
            # El SKU es único en la BD, así que .get() es seguro
            return Product.objects.get(sku=sku)
        except ObjectDoesNotExist:
            # Si no se encuentra el producto con ese SKU, retornar None
            return None
    
    @staticmethod
    def get_by_category(category_name: str) -> List[Product]:
        """
        Obtiene productos filtrados por categoría.
        
        Este método busca todos los productos que pertenecen a una categoría
        específica. La búsqueda es case-insensitive y parcial (icontains),
        así que "figuras" encontrará "Figuras", "FIGURAS", etc.
        
        Args:
            category_name: Nombre de la categoría a filtrar (string)
                          Puede ser parcial (ej: "fig" encontrará "Figuras")
            
        Returns:
            List[Product]: Lista de productos que pertenecen a la categoría,
                          ordenados alfabéticamente por nombre
                          Lista vacía si no hay productos en esa categoría
            
        Ejemplo:
            >>> products = ProductRepository.get_by_category("Figuras")
            >>> len(products)
            10
        """
        # Filtrar productos por categoría usando relación ForeignKey
        # category__category_name: accede al campo category_name de la relación Category
        # __icontains: búsqueda case-insensitive parcial
        # .order_by('product_name'): ordenar alfabéticamente
        return list(Product.objects.filter(
            category__category_name__icontains=category_name
        ).order_by('product_name'))
    
    @staticmethod
    def get_by_licence(licence_name: str) -> List[Product]:
        """
        Obtiene productos filtrados por licencia.
        
        Este método busca todos los productos que pertenecen a una licencia
        específica. La búsqueda es case-insensitive y parcial (icontains),
        así que "star" encontrará "Star Wars", "STAR WARS", etc.
        
        Args:
            licence_name: Nombre de la licencia a filtrar (string)
                        Puede ser parcial (ej: "star" encontrará "Star Wars")
            
        Returns:
            List[Product]: Lista de productos que pertenecen a la licencia,
                          ordenados alfabéticamente por nombre
                          Lista vacía si no hay productos de esa licencia
            
        Ejemplo:
            >>> products = ProductRepository.get_by_licence("Star Wars")
            >>> len(products)
            4
        """
        # Filtrar productos por licencia usando relación ForeignKey
        # licence__licence_name: accede al campo licence_name de la relación Licence
        # __icontains: búsqueda case-insensitive parcial
        # .order_by('product_name'): ordenar alfabéticamente
        return list(Product.objects.filter(
            licence__licence_name__icontains=licence_name
        ).order_by('product_name'))
    
    @staticmethod
    def sku_exists(sku: str, exclude_product_id: Optional[int] = None) -> bool:
        """
        Verifica si un SKU ya existe en la base de datos.
        
        Este método es útil para validar que un SKU sea único antes de crear
        un producto, o para verificar si un SKU está disponible al actualizar.
        
        Args:
            sku: SKU a verificar (string)
            exclude_product_id: ID del producto a excluir de la verificación
                              (útil para updates: verificar que el SKU no esté
                              en uso por OTRO producto, pero permitir el mismo
                              producto que se está actualizando)
            
        Returns:
            bool: True si el SKU existe, False si está disponible
            
        Ejemplo:
            >>> ProductRepository.sku_exists("STW001001")
            True
            >>> ProductRepository.sku_exists("NEW001001")
            False
            >>> # Al actualizar producto ID 1, excluirlo de la verificación
            >>> ProductRepository.sku_exists("STW001001", exclude_product_id=1)
            False  # No existe en otros productos
        """
        # Crear queryset con productos que tienen ese SKU
        queryset = Product.objects.filter(sku=sku)
        
        # Si se especifica un producto a excluir (útil para updates)
        if exclude_product_id:
            # Excluir ese producto del queryset
            # Esto permite verificar que el SKU no esté en uso por OTRO producto
            queryset = queryset.exclude(product_id=exclude_product_id)
        
        # Retornar True si existe al menos un producto con ese SKU
        return queryset.exists()
    
    @staticmethod
    def create(**kwargs) -> Product:
        """
        Crea un nuevo producto en la base de datos.
        
        Este método inserta un nuevo registro en la tabla 'product' con los
        datos proporcionados. Todos los campos requeridos deben estar presentes.
        
        Args:
            **kwargs: Campos del producto a crear:
                     - product_name, product_description, price, stock, sku (obligatorios)
                     - discount, dues, created_by, image_front, image_back (opcionales)
                     - additional_images (opcional, JSON string)
                     - licence: Objeto Licence (ForeignKey, obligatorio)
                     - category: Objeto Category (ForeignKey, obligatorio)
            
        Returns:
            Product: Instancia del Product creado con su ID asignado
            
        Ejemplo:
            >>> product = ProductRepository.create(
            ...     product_name="Nuevo Producto",
            ...     price=100.0,
            ...     stock=10,
            ...     sku="NEW001",
            ...     licence=licence_obj,
            ...     category=category_obj
            ... )
            >>> product.product_id
            14
        """
        # Usar .create() del ORM de Django para insertar el registro
        # Django maneja automáticamente la asignación del ID y la inserción en la BD
        return Product.objects.create(**kwargs)
    
    @staticmethod
    def update(product: Product, **kwargs) -> Product:
        """
        Actualiza un producto existente en la base de datos.
        
        Este método modifica los campos especificados de un producto existente.
        Solo se actualizan los campos proporcionados en kwargs, los demás
        permanecen sin cambios.
        
        Args:
            product: Instancia del Product a actualizar (debe existir en la BD)
            **kwargs: Campos a actualizar con sus nuevos valores
                    Solo se actualizan los campos proporcionados
                    Ejemplo: {'price': 150.0, 'stock': 20}
            
        Returns:
            Product: Instancia del Product actualizada (la misma instancia)
            
        Ejemplo:
            >>> product = ProductRepository.get_by_id(1)
            >>> updated = ProductRepository.update(product, price=150.0, stock=20)
            >>> updated.price
            150.0
        """
        # Iterar sobre todos los campos a actualizar
        for key, value in kwargs.items():
            # Usar setattr para asignar el nuevo valor al campo
            # Esto es equivalente a: product.key = value
            setattr(product, key, value)
        
        # Guardar los cambios en la base de datos
        # .save() actualiza el registro existente
        product.save()
        
        # Retornar la instancia actualizada
        return product
    
    @staticmethod
    def delete(product: Product) -> bool:
        """
        Elimina un producto de la base de datos.
        
        Este método elimina permanentemente el registro del producto de la
        base de datos. La operación no se puede deshacer.
        
        IMPORTANTE: No elimina las imágenes del sistema de archivos, solo
        el registro de la base de datos.
        
        Args:
            product: Instancia del Product a eliminar (debe existir en la BD)
            
        Returns:
            bool: Siempre retorna True si no hay error
                 (si hay error, lanza excepción)
            
        Ejemplo:
            >>> product = ProductRepository.get_by_id(1)
            >>> ProductRepository.delete(product)
            True
        """
        # Eliminar el producto de la base de datos
        # .delete() elimina el registro permanentemente
        product.delete()
        
        # Retornar True para indicar éxito
        return True

