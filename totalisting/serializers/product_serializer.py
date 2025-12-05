"""
Serializer para el modelo Product.

Convierte objetos Product a diccionarios JSON y viceversa.
"""

from typing import Dict, Any, Optional
import json
from ..models import Product


def _parse_additional_images(value) -> Optional[str]:
    """
    Parsea additional_images que puede venir como:
    - String JSON: '["/path1", "/path2"]'
    - Lista Python: ["/path1", "/path2"]
    - None o vacío
    
    Retorna string JSON válido o None.
    """
    if not value:
        return None
    
    if isinstance(value, str):
        # Si ya es string, verificar si es JSON válido
        try:
            parsed = json.loads(value)
            # Si se puede parsear, retornarlo como JSON string
            return json.dumps(parsed) if parsed else None
        except (json.JSONDecodeError, TypeError):
            # Si no es JSON válido, retornar None
            return None
    
    if isinstance(value, (list, dict)):
        # Si es lista o dict, convertir a JSON string
        return json.dumps(value) if value else None
    
    return None


class ProductSerializer:
    """Serializer para productos."""
    
    @staticmethod
    def to_dict(product: Product, include_relations: bool = True) -> Dict[str, Any]:
        """
        Convierte un objeto Product a diccionario.
        
        Args:
            product: Instancia del modelo Product
            include_relations: Si True, incluye información de licencia y categoría
            
        Returns:
            Diccionario con los datos del producto
        """
        data = {
            'product_id': product.product_id,
            'product_name': product.product_name,
            'product_description': product.product_description,
            'price': float(product.price),
            'stock': product.stock,
            'discount': product.discount or 0,
            'sku': product.sku,
            'image_front': product.image_front or '',
            'image_back': product.image_back or '',
        }
        
        # Agregar imágenes adicionales si existen
        if hasattr(product, 'additional_images') and product.additional_images:
            try:
                import json
                data['additional_images'] = json.loads(product.additional_images)
            except:
                data['additional_images'] = []
        
        if include_relations:
            if hasattr(product, 'licence') and product.licence:
                data['licence'] = {
                    'licence_id': product.licence.licence_id,
                    'licence_name': product.licence.licence_name,
                }
            
            if hasattr(product, 'category') and product.category:
                data['category'] = {
                    'category_id': product.category.category_id,
                    'category_name': product.category.category_name,
                }
        
        return data
    
    @staticmethod
    def to_dict_list(products, include_relations: bool = False) -> list:
        """
        Convierte una lista de productos a lista de diccionarios.
        
        Args:
            products: QuerySet o lista de productos
            include_relations: Si True, incluye información de relaciones
            
        Returns:
            Lista de diccionarios con los datos de los productos
        """
        return [ProductSerializer.to_dict(product, include_relations) for product in products]
    
    @staticmethod
    def validate_create_data(data: Dict[str, Any]) -> tuple[bool, Optional[str], Dict[str, Any]]:
        """
        Valida los datos para crear un producto.
        
        Args:
            data: Diccionario con los datos del producto
            
        Returns:
            Tupla (es_valido, mensaje_error, datos_validados)
        """
        required_fields = ['product_name', 'product_description', 'price', 'stock', 'sku', 'licence', 'category']
        missing_fields = [field for field in required_fields if not data.get(field) and not data.get(f'{field}_name')]
        
        if missing_fields:
            return False, f'Faltan campos obligatorios: {", ".join(missing_fields)}', {}
        
        # Validar tipos de datos
        try:
            # Manejar licencia y categoría por ID o nombre
            licence_id = data.get('licence_id')
            category_id = data.get('category_id')
            licence_name = data.get('licence') or data.get('licence_name')
            category_name = data.get('category') or data.get('category_name')
            
            validated_data = {
                'product_name': str(data.get('product_name', '')),
                'product_description': str(data.get('product_description', '')),
                'price': float(data.get('price', 0)),
                'stock': int(data.get('stock', 0)),
                'discount': int(data.get('discount', 0)) if data.get('discount') else None,
                'sku': str(data.get('sku', '')),
                'licence_id': int(licence_id) if licence_id else None,
                'licence_name': licence_name,
                'category_id': int(category_id) if category_id else None,
                'category_name': category_name,
                'image_front': data.get('image_front', ''),
                'image_back': data.get('image_back', ''),
                'additional_images': _parse_additional_images(data.get('additional_images', '')),
                'created_by': int(data.get('created_by', 1)),
                'dues': int(data.get('dues')) if data.get('dues') else None,
            }
            return True, None, validated_data
        except (ValueError, TypeError) as e:
            return False, f'Error en los tipos de datos: {str(e)}', {}

