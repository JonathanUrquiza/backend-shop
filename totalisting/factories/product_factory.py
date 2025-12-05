"""
Factory para crear productos.

Encapsula la lógica de creación de productos con sus relaciones.
"""

from typing import Dict, Any, Optional
from ..models import Product, Licence, Category
from ..repositories.licence_repository import LicenceRepository
from ..repositories.category_repository import CategoryRepository
from ..repositories.product_repository import ProductRepository


class ProductFactory:
    """Factory para crear productos."""
    
    @staticmethod
    def create_product(data: Dict[str, Any]) -> tuple[Optional[Product], Optional[str], Dict[str, Any]]:
        """
        Crea un producto con sus relaciones (licencia y categoría).
        
        Si la licencia o categoría no existen, las crea automáticamente.
        
        Args:
            data: Diccionario con los datos del producto
            
        Returns:
            Tupla (producto, mensaje_error, metadata)
            metadata contiene información sobre licencia y categoría creadas
        """
        # Validar datos
        from ..serializers.product_serializer import ProductSerializer
        is_valid, error_message, validated_data = ProductSerializer.validate_create_data(data)
        
        if not is_valid:
            return None, error_message, {}
        
        # Verificar si el SKU ya existe
        if ProductRepository.sku_exists(validated_data['sku']):
            return None, f"El SKU '{validated_data['sku']}' ya existe en la base de datos", {}
        
        # Obtener licencia por ID o nombre
        if validated_data.get('licence_id'):
            licence_obj = LicenceRepository.get_by_id(validated_data['licence_id'])
            if not licence_obj:
                return None, f'Licencia con ID {validated_data["licence_id"]} no encontrada', {}
            licence_created = False
        else:
            licence_obj, licence_created = LicenceRepository.get_or_create(
                validated_data['licence_name'],
                defaults={
                    'licence_description': data.get('licence_description', f'Licencia {validated_data["licence_name"]}'),
                    'licence_image': data.get('licence_image', '')
                }
            )
        
        # Obtener categoría por ID o nombre
        if validated_data.get('category_id'):
            category_obj = CategoryRepository.get_by_id(validated_data['category_id'])
            if not category_obj:
                return None, f'Categoría con ID {validated_data["category_id"]} no encontrada', {}
            category_created = False
        else:
            category_obj, category_created = CategoryRepository.get_or_create(
                validated_data['category_name'],
                defaults={
                    'category_description': data.get('category_description', f'Categoría {validated_data["category_name"]}'),
                    'image_category': data.get('image_category', '')
                }
            )
        
        # Crear el producto
        try:
            create_kwargs = {
                'product_name': validated_data['product_name'],
                'product_description': validated_data['product_description'],
                'price': validated_data['price'],
                'stock': validated_data['stock'],
                'discount': validated_data['discount'],
                'sku': validated_data['sku'],
                'dues': validated_data['dues'],
                'created_by': validated_data['created_by'],
                'image_front': validated_data['image_front'],
                'image_back': validated_data['image_back'],
                'licence': licence_obj,
                'category': category_obj,
            }
            
            # Agregar imágenes adicionales si existen
            if validated_data.get('additional_images'):
                create_kwargs['additional_images'] = validated_data['additional_images']
            
            product = ProductRepository.create(**create_kwargs)
            
            metadata = {
                'licence': {
                    'id': licence_obj.licence_id,
                    'name': licence_obj.licence_name,
                    'created': licence_created
                },
                'category': {
                    'id': category_obj.category_id,
                    'name': category_obj.category_name,
                    'created': category_created
                }
            }
            
            return product, None, metadata
            
        except Exception as e:
            return None, f'Error al crear el producto: {str(e)}', {}

