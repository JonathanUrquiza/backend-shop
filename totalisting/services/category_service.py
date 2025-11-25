"""
Servicio para la lógica de negocio de categorías.

Separa la lógica de negocio de las vistas HTTP.
"""

from typing import Dict, Any, Optional, List
from ..models import Category
from ..repositories.category_repository import CategoryRepository
from ..serializers.category_serializer import CategorySerializer


class CategoryService:
    """Servicio para categorías."""
    
    @staticmethod
    def get_all_categories() -> List[Dict[str, Any]]:
        """
        Obtiene todas las categorías.
        
        Returns:
            Lista de diccionarios con los datos de las categorías
        """
        categories = CategoryRepository.get_all()
        return CategorySerializer.to_dict_list(categories)
    
    @staticmethod
    def get_categories_by_licence(licence_name: str) -> List[Dict[str, Any]]:
        """
        Obtiene categorías filtradas por licencia.
        
        Args:
            licence_name: Nombre de la licencia
            
        Returns:
            Lista de diccionarios con los datos de las categorías
        """
        categories = CategoryRepository.get_by_licence(licence_name)
        return CategorySerializer.to_dict_list(categories)
    
    @staticmethod
    def update_category(category_id: int, data: Dict[str, Any]) -> tuple[Optional[Category], Optional[str]]:
        """
        Actualiza una categoría existente.
        
        Args:
            category_id: ID de la categoría a actualizar
            data: Diccionario con los campos a actualizar
            
        Returns:
            Tupla (categoría_actualizada, mensaje_error)
        """
        category = CategoryRepository.get_by_id(category_id)
        if not category:
            return None, 'Categoría no encontrada'
        
        update_data = {}
        if 'category_name' in data:
            update_data['category_name'] = data['category_name']
        if 'category_description' in data:
            update_data['category_description'] = data.get('category_description', '')
        
        try:
            updated_category = CategoryRepository.update(category, **update_data)
            return updated_category, None
        except Exception as e:
            return None, f'Error al actualizar la categoría: {str(e)}'
    
    @staticmethod
    def delete_category(category_id: int) -> tuple[bool, Optional[str], Optional[Dict[str, Any]]]:
        """
        Elimina una categoría.
        
        Args:
            category_id: ID de la categoría a eliminar
            
        Returns:
            Tupla (exito, mensaje_error, datos_de_la_categoría_eliminada)
        """
        category = CategoryRepository.get_by_id(category_id)
        if not category:
            return False, 'Categoría no encontrada', None
        
        # Verificar si tiene productos asociados
        products_count = CategoryRepository.count_products(category)
        if products_count > 0:
            return False, f'No se puede eliminar la categoría porque tiene {products_count} producto(s) asociado(s)', {
                'category_id': category.category_id,
                'products_count': products_count
            }
        
        category_data = {
            'category_id': category.category_id,
            'category_name': category.category_name
        }
        
        try:
            CategoryRepository.delete(category)
            return True, None, category_data
        except Exception as e:
            return False, f'Error al eliminar la categoría: {str(e)}', None

