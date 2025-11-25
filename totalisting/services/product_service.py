"""
Servicio para la lógica de negocio de productos.

Separa la lógica de negocio de las vistas HTTP.
"""

from typing import Dict, Any, Optional, List
from ..models import Product
from ..repositories.product_repository import ProductRepository
from ..repositories.licence_repository import LicenceRepository
from ..repositories.category_repository import CategoryRepository
from ..serializers.product_serializer import ProductSerializer
from ..factories.product_factory import ProductFactory


class ProductService:
    """Servicio para productos."""
    
    @staticmethod
    def create_product(data: Dict[str, Any]) -> tuple[Optional[Product], Optional[str], Dict[str, Any]]:
        """
        Crea un nuevo producto.
        
        Args:
            data: Diccionario con los datos del producto
            
        Returns:
            Tupla (producto, mensaje_error, metadata)
        """
        return ProductFactory.create_product(data)
    
    @staticmethod
    def get_all_products() -> List[Dict[str, Any]]:
        """
        Obtiene todos los productos.
        
        Returns:
            Lista de diccionarios con los datos de los productos
        """
        products = ProductRepository.get_all()
        return ProductSerializer.to_dict_list(products, include_relations=False)
    
    @staticmethod
    def get_product_by_id(product_id: int) -> tuple[Optional[Dict[str, Any]], Optional[str]]:
        """
        Obtiene un producto por su ID.
        
        Args:
            product_id: ID del producto
            
        Returns:
            Tupla (datos_del_producto, mensaje_error)
        """
        product = ProductRepository.get_by_id(product_id)
        if not product:
            return None, 'Producto no encontrado'
        
        return ProductSerializer.to_dict(product, include_relations=True), None
    
    @staticmethod
    def get_product_by_name(product_name: str) -> tuple[Optional[Dict[str, Any]], Optional[str]]:
        """
        Obtiene un producto por su nombre.
        
        Args:
            product_name: Nombre del producto
            
        Returns:
            Tupla (datos_del_producto, mensaje_error)
        """
        product = ProductRepository.get_by_name(product_name)
        if not product:
            return None, 'Producto no encontrado'
        
        return ProductSerializer.to_dict(product, include_relations=True), None
    
    @staticmethod
    def get_product_by_sku(sku: str) -> tuple[Optional[Dict[str, Any]], Optional[str]]:
        """
        Obtiene un producto por su SKU.
        
        Args:
            sku: SKU del producto
            
        Returns:
            Tupla (datos_del_producto, mensaje_error)
        """
        product = ProductRepository.get_by_sku(sku)
        if not product:
            return None, 'Producto no encontrado'
        
        return ProductSerializer.to_dict(product, include_relations=True), None
    
    @staticmethod
    def get_products_by_category(category_name: str) -> List[Dict[str, Any]]:
        """
        Obtiene productos filtrados por categoría.
        
        Args:
            category_name: Nombre de la categoría
            
        Returns:
            Lista de diccionarios con los datos de los productos
        """
        products = ProductRepository.get_by_category(category_name)
        return ProductSerializer.to_dict_list(products, include_relations=False)
    
    @staticmethod
    def get_products_by_licence(licence_name: str) -> List[Dict[str, Any]]:
        """
        Obtiene productos filtrados por licencia.
        
        Args:
            licence_name: Nombre de la licencia
            
        Returns:
            Lista de diccionarios con los datos de los productos
        """
        products = ProductRepository.get_by_licence(licence_name)
        return ProductSerializer.to_dict_list(products, include_relations=False)
    
    @staticmethod
    def update_product(product_id: int, data: Dict[str, Any]) -> tuple[Optional[Product], Optional[str]]:
        """
        Actualiza un producto existente.
        
        Args:
            product_id: ID del producto a actualizar
            data: Diccionario con los campos a actualizar
            
        Returns:
            Tupla (producto_actualizado, mensaje_error)
        """
        product = ProductRepository.get_by_id(product_id)
        if not product:
            return None, 'Producto no encontrado'
        
        # Validar SKU si se está actualizando
        if 'sku' in data:
            new_sku = data['sku']
            if new_sku != product.sku and ProductRepository.sku_exists(new_sku, exclude_product_id=product_id):
                return None, f"El SKU '{new_sku}' ya está en uso por otro producto"
        
        # Actualizar licencia si se proporciona
        if 'licence' in data or 'licence_name' in data:
            licence_name = data.get('licence') or data.get('licence_name')
            licence_obj, _ = LicenceRepository.get_or_create(
                licence_name,
                defaults={
                    'licence_description': data.get('licence_description', f'Licencia {licence_name}'),
                    'licence_image': data.get('licence_image', '')
                }
            )
            data['licence'] = licence_obj
        
        # Actualizar categoría si se proporciona
        if 'category' in data or 'category_name' in data:
            category_name = data.get('category') or data.get('category_name')
            category_obj, _ = CategoryRepository.get_or_create(
                category_name,
                defaults={
                    'category_description': data.get('category_description', f'Categoría {category_name}')
                }
            )
            data['category'] = category_obj
        
        # Preparar datos para actualización
        update_data = {}
        fields_to_update = ['product_name', 'product_description', 'price', 'stock', 
                          'discount', 'sku', 'image_front', 'image_back', 'dues', 'created_by', 
                          'licence', 'category']
        
        for field in fields_to_update:
            if field in data:
                if field == 'price':
                    update_data[field] = float(data[field])
                elif field in ['stock', 'discount', 'dues', 'created_by']:
                    update_data[field] = int(data[field]) if data[field] else None
                else:
                    update_data[field] = data[field]
        
        try:
            updated_product = ProductRepository.update(product, **update_data)
            return updated_product, None
        except ValueError as e:
            return None, f'Error en los tipos de datos: {str(e)}'
        except Exception as e:
            return None, f'Error al actualizar el producto: {str(e)}'
    
    @staticmethod
    def delete_product(product_id: int) -> tuple[bool, Optional[str], Optional[Dict[str, Any]]]:
        """
        Elimina un producto.
        
        Args:
            product_id: ID del producto a eliminar
            
        Returns:
            Tupla (exito, mensaje_error, datos_del_producto_eliminado)
        """
        product = ProductRepository.get_by_id(product_id)
        if not product:
            return False, 'Producto no encontrado', None
        
        product_data = {
            'product_id': product.product_id,
            'product_name': product.product_name
        }
        
        try:
            ProductRepository.delete(product)
            return True, None, product_data
        except Exception as e:
            return False, f'Error al eliminar el producto: {str(e)}', None

