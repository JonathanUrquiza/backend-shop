"""
Repositorio para el modelo Product.

Abstrae el acceso a datos de productos.
"""

from typing import Optional, List
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from ..models import Product


class ProductRepository:
    """Repositorio para productos."""
    
    @staticmethod
    def get_all() -> List[Product]:
        """Obtiene todos los productos ordenados por nombre."""
        return list(Product.objects.all().order_by('product_name'))
    
    @staticmethod
    def get_by_id(product_id: int) -> Optional[Product]:
        """
        Obtiene un producto por su ID.
        
        Args:
            product_id: ID del producto
            
        Returns:
            Producto si existe, None en caso contrario
        """
        try:
            return Product.objects.get(product_id=product_id)
        except ObjectDoesNotExist:
            return None
    
    @staticmethod
    def get_by_name(product_name: str) -> Optional[Product]:
        """
        Obtiene un producto por su nombre.
        
        Args:
            product_name: Nombre del producto
            
        Returns:
            Producto si existe, None en caso contrario
        """
        try:
            return Product.objects.get(product_name=product_name)
        except ObjectDoesNotExist:
            return None
        except MultipleObjectsReturned:
            return None
    
    @staticmethod
    def get_by_sku(sku: str) -> Optional[Product]:
        """
        Obtiene un producto por su SKU.
        
        Args:
            sku: SKU del producto
            
        Returns:
            Producto si existe, None en caso contrario
        """
        try:
            return Product.objects.get(sku=sku)
        except ObjectDoesNotExist:
            return None
    
    @staticmethod
    def get_by_category(category_name: str) -> List[Product]:
        """
        Obtiene productos filtrados por categoría.
        
        Args:
            category_name: Nombre de la categoría
            
        Returns:
            Lista de productos
        """
        return list(Product.objects.filter(
            category__category_name__icontains=category_name
        ).order_by('product_name'))
    
    @staticmethod
    def get_by_licence(licence_name: str) -> List[Product]:
        """
        Obtiene productos filtrados por licencia.
        
        Args:
            licence_name: Nombre de la licencia
            
        Returns:
            Lista de productos
        """
        return list(Product.objects.filter(
            licence__licence_name__icontains=licence_name
        ).order_by('product_name'))
    
    @staticmethod
    def sku_exists(sku: str, exclude_product_id: Optional[int] = None) -> bool:
        """
        Verifica si un SKU ya existe.
        
        Args:
            sku: SKU a verificar
            exclude_product_id: ID del producto a excluir de la verificación (útil para updates)
            
        Returns:
            True si el SKU existe, False en caso contrario
        """
        queryset = Product.objects.filter(sku=sku)
        if exclude_product_id:
            queryset = queryset.exclude(product_id=exclude_product_id)
        return queryset.exists()
    
    @staticmethod
    def create(**kwargs) -> Product:
        """
        Crea un nuevo producto.
        
        Args:
            **kwargs: Campos del producto
            
        Returns:
            Producto creado
        """
        return Product.objects.create(**kwargs)
    
    @staticmethod
    def update(product: Product, **kwargs) -> Product:
        """
        Actualiza un producto existente.
        
        Args:
            product: Instancia del producto a actualizar
            **kwargs: Campos a actualizar
            
        Returns:
            Producto actualizado
        """
        for key, value in kwargs.items():
            setattr(product, key, value)
        product.save()
        return product
    
    @staticmethod
    def delete(product: Product) -> bool:
        """
        Elimina un producto.
        
        Args:
            product: Instancia del producto a eliminar
            
        Returns:
            True si se eliminó correctamente
        """
        product.delete()
        return True

