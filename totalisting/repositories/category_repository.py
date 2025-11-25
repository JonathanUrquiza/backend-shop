"""
Repositorio para el modelo Category.

Abstrae el acceso a datos de categorías.
"""

from typing import Optional, List
from django.core.exceptions import ObjectDoesNotExist
from ..models import Category, Product


class CategoryRepository:
    """Repositorio para categorías."""
    
    @staticmethod
    def get_all() -> List[Category]:
        """Obtiene todas las categorías ordenadas por nombre."""
        return list(Category.objects.all().order_by('category_name'))
    
    @staticmethod
    def get_by_id(category_id: int) -> Optional[Category]:
        """
        Obtiene una categoría por su ID.
        
        Args:
            category_id: ID de la categoría
            
        Returns:
            Categoría si existe, None en caso contrario
        """
        try:
            return Category.objects.get(category_id=category_id)
        except ObjectDoesNotExist:
            return None
    
    @staticmethod
    def get_by_name(category_name: str) -> Optional[Category]:
        """
        Obtiene una categoría por su nombre.
        
        Args:
            category_name: Nombre de la categoría
            
        Returns:
            Categoría si existe, None en caso contrario
        """
        try:
            return Category.objects.get(category_name=category_name)
        except ObjectDoesNotExist:
            return None
    
    @staticmethod
    def get_by_licence(licence_name: str) -> List[Category]:
        """
        Obtiene categorías filtradas por licencia.
        
        Args:
            licence_name: Nombre de la licencia
            
        Returns:
            Lista de categorías
        """
        return list(Category.objects.filter(
            product__licence__licence_name__icontains=licence_name
        ).distinct().order_by('category_name'))
    
    @staticmethod
    def get_or_create(category_name: str, defaults: Optional[dict] = None) -> tuple[Category, bool]:
        """
        Obtiene o crea una categoría.
        
        Args:
            category_name: Nombre de la categoría
            defaults: Valores por defecto para crear la categoría
            
        Returns:
            Tupla (categoría, creada)
        """
        # Usar filter().first() para evitar problemas con múltiples objetos
        existing = Category.objects.filter(category_name=category_name).first()
        if existing:
            return existing, False
        
        # Crear nueva categoría
        new_category = Category.objects.create(
            category_name=category_name,
            **(defaults or {})
        )
        return new_category, True
    
    @staticmethod
    def update(category: Category, **kwargs) -> Category:
        """
        Actualiza una categoría existente.
        
        Args:
            category: Instancia de la categoría a actualizar
            **kwargs: Campos a actualizar
            
        Returns:
            Categoría actualizada
        """
        for key, value in kwargs.items():
            setattr(category, key, value)
        category.save()
        return category
    
    @staticmethod
    def delete(category: Category) -> bool:
        """
        Elimina una categoría.
        
        Args:
            category: Instancia de la categoría a eliminar
            
        Returns:
            True si se eliminó correctamente
        """
        category.delete()
        return True
    
    @staticmethod
    def has_products(category: Category) -> bool:
        """
        Verifica si una categoría tiene productos asociados.
        
        Args:
            category: Instancia de la categoría
            
        Returns:
            True si tiene productos, False en caso contrario
        """
        return Product.objects.filter(category=category).exists()
    
    @staticmethod
    def count_products(category: Category) -> int:
        """
        Cuenta los productos asociados a una categoría.
        
        Args:
            category: Instancia de la categoría
            
        Returns:
            Número de productos asociados
        """
        return Product.objects.filter(category=category).count()

