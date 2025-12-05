"""
Repositorio para el modelo Category.

Este módulo contiene la clase CategoryRepository que abstrae todas las operaciones
de acceso a datos relacionadas con categorías. Implementa el Repository Pattern
que separa la lógica de acceso a datos de la lógica de negocio.

El repositorio proporciona métodos para:
- Obtener categorías (todas, por ID, por nombre, filtradas por licencia)
- Crear categorías (con get_or_create para evitar duplicados)
- Actualizar categorías
- Eliminar categorías
- Verificar relaciones con productos

Todas las consultas a la base de datos relacionadas con categorías deben pasar
por este repositorio, no acceder directamente al modelo Category.
"""

# Importar tipos de Python para type hints
from typing import Optional, List
# Importar excepciones de Django para manejo de errores de base de datos
from django.core.exceptions import ObjectDoesNotExist
# Importar los modelos Category y Product para trabajar con instancias
from ..models import Category, Product


class CategoryRepository:
    """
    Repositorio para categorías.
    
    Esta clase encapsula todas las operaciones de acceso a datos relacionadas
    con categorías. Proporciona una interfaz limpia y consistente para interactuar
    con la tabla 'category' de la base de datos.
    
    Todos los métodos son estáticos, lo que significa que no se necesita
    instanciar la clase para usarlos.
    """
    
    @staticmethod
    def get_all() -> List[Category]:
        """
        Obtiene todas las categorías ordenadas por nombre.
        
        Este método retorna todas las categorías de la base de datos ordenadas
        alfabéticamente por nombre. Es útil para listar todas las categorías
        disponibles en el sistema.
        
        Returns:
            List[Category]: Lista de todas las categorías ordenadas por nombre
                          Lista vacía si no hay categorías
        
        Ejemplo:
            >>> categories = CategoryRepository.get_all()
            >>> len(categories)
            5
        """
        # Obtener todas las categorías usando el ORM de Django
        # .all() obtiene todos los registros
        # .order_by('category_name') ordena alfabéticamente por nombre
        # list() convierte el QuerySet a lista de Python
        return list(Category.objects.all().order_by('category_name'))
    
    @staticmethod
    def get_by_id(category_id: int) -> Optional[Category]:
        """
        Obtiene una categoría por su ID.
        
        Este método busca una categoría específica usando su ID único.
        Es el método más eficiente para obtener una categoría cuando se conoce su ID.
        
        Args:
            category_id: ID único de la categoría a buscar (número entero)
            
        Returns:
            Optional[Category]: Instancia del Category si existe, None si no se encuentra
            
        Ejemplo:
            >>> category = CategoryRepository.get_by_id(1)
            >>> if category:
            ...     print(category.category_name)
            'Figuras'
        """
        try:
            # Usar .get() para obtener un único registro por ID
            # .get() lanza excepción si no encuentra o encuentra múltiples
            return Category.objects.get(category_id=category_id)
        except ObjectDoesNotExist:
            # Si la categoría no existe, retornar None en lugar de lanzar excepción
            # Esto hace el código más robusto y fácil de manejar
            return None
    
    @staticmethod
    def get_by_name(category_name: str) -> Optional[Category]:
        """
        Obtiene una categoría por su nombre exacto.
        
        Este método busca una categoría por su nombre exacto (case-sensitive).
        Útil para verificar si una categoría ya existe antes de crearla.
        
        Args:
            category_name: Nombre exacto de la categoría a buscar (string)
            
        Returns:
            Optional[Category]: Instancia del Category si existe, None si no se encuentra
            
        Ejemplo:
            >>> category = CategoryRepository.get_by_name("Figuras")
            >>> if category:
            ...     print(category.category_id)
            1
        """
        try:
            # Buscar categoría por nombre exacto
            # .get() requiere coincidencia exacta del nombre
            return Category.objects.get(category_name=category_name)
        except ObjectDoesNotExist:
            # Si no se encuentra la categoría, retornar None
            return None
    
    @staticmethod
    def get_by_licence(licence_name: str) -> List[Category]:
        """
        Obtiene categorías filtradas por licencia.
        
        Este método busca todas las categorías que tienen al menos un producto
        asociado a una licencia específica. Es útil para mostrar categorías
        disponibles cuando se filtra por licencia.
        
        Args:
            licence_name: Nombre de la licencia a filtrar (string)
                        Puede ser parcial (ej: "star" encontrará "Star Wars")
            
        Returns:
            List[Category]: Lista de categorías que tienen productos de esa licencia,
                          ordenadas alfabéticamente por nombre
                          Lista vacía si no hay categorías con productos de esa licencia
            
        Ejemplo:
            >>> categories = CategoryRepository.get_by_licence("Star Wars")
            >>> len(categories)
            3
        """
        # Filtrar categorías que tienen productos con la licencia especificada
        # product__licence__licence_name: accede al nombre de la licencia a través de la relación
        # __icontains: búsqueda case-insensitive parcial
        # .distinct(): elimina categorías duplicadas (si una categoría tiene múltiples productos)
        # .order_by('category_name'): ordenar alfabéticamente
        return list(Category.objects.filter(
            product__licence__licence_name__icontains=licence_name
        ).distinct().order_by('category_name'))
    
    @staticmethod
    def get_or_create(category_name: str, defaults: Optional[dict] = None) -> tuple[Category, bool]:
        """
        Obtiene o crea una categoría.
        
        Este método busca una categoría por nombre, y si no existe, la crea.
        Es útil para evitar duplicados y crear categorías automáticamente cuando
        se necesita (ej: al crear un producto con una categoría nueva).
        
        Args:
            category_name: Nombre de la categoría a buscar o crear (string)
            defaults: Diccionario con valores por defecto para crear la categoría
                     (ej: {'category_description': '...', 'image_category': '...'})
            
        Returns:
            tuple[Category, bool]: 
            - Category: Instancia de la categoría (existente o recién creada)
            - bool: True si se creó, False si ya existía
            
        Ejemplo:
            >>> category, created = CategoryRepository.get_or_create(
            ...     "Nueva Categoría",
            ...     defaults={'category_description': 'Descripción'}
            ... )
            >>> created
            True  # Se creó nueva
        """
        # Usar filter().first() para evitar problemas con múltiples objetos
        # Buscar categoría existente por nombre exacto
        existing = Category.objects.filter(category_name=category_name).first()
        
        if existing:
            # Si existe, retornar la categoría existente y False (no se creó)
            return existing, False
        
        # Si no existe, crear nueva categoría
        # Usar defaults si se proporcionaron, sino usar diccionario vacío
        new_category = Category.objects.create(
            category_name=category_name,  # Nombre de la categoría (obligatorio)
            **(defaults or {})  # Desempaquetar valores por defecto si existen
        )
        
        # Retornar la categoría creada y True (se creó)
        return new_category, True
    
    @staticmethod
    def update(category: Category, **kwargs) -> Category:
        """
        Actualiza una categoría existente en la base de datos.
        
        Este método modifica los campos especificados de una categoría existente.
        Solo se actualizan los campos proporcionados en kwargs, los demás
        permanecen sin cambios.
        
        Args:
            category: Instancia del Category a actualizar (debe existir en la BD)
            **kwargs: Campos a actualizar con sus nuevos valores
                    Solo se actualizan los campos proporcionados
                    Ejemplo: {'category_description': 'Nueva descripción'}
            
        Returns:
            Category: Instancia del Category actualizada (la misma instancia)
            
        Ejemplo:
            >>> category = CategoryRepository.get_by_id(1)
            >>> updated = CategoryRepository.update(category, category_description='Nueva desc')
            >>> updated.category_description
            'Nueva desc'
        """
        # Iterar sobre todos los campos a actualizar
        for key, value in kwargs.items():
            # Usar setattr para asignar el nuevo valor al campo
            # Esto es equivalente a: category.key = value
            setattr(category, key, value)
        
        # Guardar los cambios en la base de datos
        # .save() actualiza el registro existente
        category.save()
        
        # Retornar la instancia actualizada
        return category
    
    @staticmethod
    def delete(category: Category) -> bool:
        """
        Elimina una categoría de la base de datos.
        
        Este método elimina permanentemente el registro de la categoría de la
        base de datos. La operación no se puede deshacer.
        
        IMPORTANTE: No elimina los productos asociados, solo el registro de la categoría.
        Los productos quedarán sin categoría (o con categoría NULL dependiendo de la BD).
        
        Args:
            category: Instancia del Category a eliminar (debe existir en la BD)
            
        Returns:
            bool: Siempre retorna True si no hay error
                 (si hay error, lanza excepción)
            
        Ejemplo:
            >>> category = CategoryRepository.get_by_id(1)
            >>> CategoryRepository.delete(category)
            True
        """
        # Eliminar la categoría de la base de datos
        # .delete() elimina el registro permanentemente
        category.delete()
        
        # Retornar True para indicar éxito
        return True
    
    @staticmethod
    def has_products(category: Category) -> bool:
        """
        Verifica si una categoría tiene productos asociados.
        
        Este método es útil para validar antes de eliminar una categoría,
        ya que normalmente no se debería eliminar una categoría que tiene productos.
        
        Args:
            category: Instancia del Category a verificar
            
        Returns:
            bool: True si tiene al menos un producto asociado, False si no tiene productos
            
        Ejemplo:
            >>> category = CategoryRepository.get_by_id(1)
            >>> CategoryRepository.has_products(category)
            True
        """
        # Verificar si existe al menos un producto con esta categoría
        # .exists() es más eficiente que .count() > 0 porque se detiene al encontrar el primero
        return Product.objects.filter(category=category).exists()
    
    @staticmethod
    def count_products(category: Category) -> int:
        """
        Cuenta los productos asociados a una categoría.
        
        Este método cuenta cuántos productos pertenecen a una categoría específica.
        Útil para mostrar estadísticas o validar antes de eliminar.
        
        Args:
            category: Instancia del Category a contar
            
        Returns:
            int: Número de productos asociados a esta categoría
                0 si no tiene productos
            
        Ejemplo:
            >>> category = CategoryRepository.get_by_id(1)
            >>> CategoryRepository.count_products(category)
            15
        """
        # Contar productos que tienen esta categoría asociada
        # .count() retorna el número total de productos
        return Product.objects.filter(category=category).count()

