"""
Serializer para el modelo Category.

Convierte objetos Category a diccionarios JSON.
"""

from typing import Dict, Any
from ..models import Category


class CategorySerializer:
    """Serializer para categorías."""
    
    @staticmethod
    def to_dict(category: Category) -> Dict[str, Any]:
        """
        Convierte un objeto Category a diccionario.
        
        Args:
            category: Instancia del modelo Category
            
        Returns:
            Diccionario con los datos de la categoría
        """
        return {
            'category_id': category.category_id,
            'category_name': category.category_name,
            'category_description': category.category_description or '',
            'image_category': category.image_category or '',
        }
    
    @staticmethod
    def to_dict_list(categories) -> list:
        """
        Convierte una lista de categorías a lista de diccionarios.
        
        Args:
            categories: QuerySet o lista de categorías
            
        Returns:
            Lista de diccionarios con los datos de las categorías
        """
        return [CategorySerializer.to_dict(category) for category in categories]

