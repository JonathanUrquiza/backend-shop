"""
Serializer para el modelo Category.

Este módulo contiene la clase CategorySerializer que se encarga de convertir
objetos Category (modelos Django) a diccionarios JSON que pueden ser enviados
al frontend.

El serializer actúa como una capa de transformación entre los modelos de Django
y las representaciones JSON que se envían al frontend.
"""

# Importar tipos de Python para type hints
from typing import Dict, Any
# Importar el modelo Category para trabajar con instancias
from ..models import Category


class CategorySerializer:
    """
    Serializer para categorías.
    
    Esta clase proporciona métodos estáticos para convertir objetos Category
    (modelos Django) a diccionarios JSON.
    
    Los métodos principales son:
    - to_dict: Convierte un Category a diccionario
    - to_dict_list: Convierte una lista de Categories a lista de diccionarios
    """
    
    @staticmethod
    def to_dict(category: Category) -> Dict[str, Any]:
        """
        Convierte un objeto Category a diccionario JSON.
        
        Este método serializa un objeto Category de Django a un diccionario Python
        que puede ser fácilmente convertido a JSON para enviar al frontend.
        
        Args:
            category: Instancia del modelo Category a serializar
            
        Returns:
            Dict[str, Any]: Diccionario con los datos de la categoría en formato JSON-friendly
            
        Ejemplo de retorno:
        {
            'category_id': 1,
            'category_name': 'Figuras',
            'category_description': 'Figuras coleccionables',
            'image_category': '/categories/figuras.webp'
        }
        """
        return {
            'category_id': category.category_id,  # ID único de la categoría
            'category_name': category.category_name,  # Nombre de la categoría
            'category_description': category.category_description or '',  # Descripción (vacío si None)
            'image_category': category.image_category or '',  # Ruta de la imagen (vacío si None)
        }
    
    @staticmethod
    def to_dict_list(categories) -> list:
        """
        Convierte una lista de categorías a lista de diccionarios JSON.
        
        Este método es útil para serializar múltiples categorías a la vez,
        como cuando se lista todas las categorías disponibles.
        
        Args:
            categories: QuerySet de Django o lista de objetos Category
                      Puede ser el resultado de Category.objects.all() o cualquier filtro
            
        Returns:
            list: Lista de diccionarios, cada uno representando una categoría
            
        Ejemplo:
            >>> categories = Category.objects.all()
            >>> CategorySerializer.to_dict_list(categories)
            [{'category_id': 1, 'category_name': '...', ...}, ...]
        """
        # Usar list comprehension para convertir cada categoría a diccionario
        # Esto es más eficiente que un loop explícito
        return [CategorySerializer.to_dict(category) for category in categories]

