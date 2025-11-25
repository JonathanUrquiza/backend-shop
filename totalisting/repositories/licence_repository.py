"""
Repositorio para el modelo Licence.

Abstrae el acceso a datos de licencias.
"""

from typing import Optional, List
from django.core.exceptions import ObjectDoesNotExist
from ..models import Licence, Product


class LicenceRepository:
    """Repositorio para licencias."""
    
    @staticmethod
    def get_all() -> List[Licence]:
        """Obtiene todas las licencias ordenadas por ID."""
        return list(Licence.objects.all().order_by('licence_id'))
    
    @staticmethod
    def get_by_id(licence_id: int) -> Optional[Licence]:
        """
        Obtiene una licencia por su ID.
        
        Args:
            licence_id: ID de la licencia
            
        Returns:
            Licencia si existe, None en caso contrario
        """
        try:
            return Licence.objects.get(licence_id=licence_id)
        except ObjectDoesNotExist:
            return None
    
    @staticmethod
    def get_by_name(licence_name: str) -> List[Licence]:
        """
        Obtiene licencias filtradas por nombre.
        
        Args:
            licence_name: Nombre de la licencia
            
        Returns:
            Lista de licencias
        """
        return list(Licence.objects.filter(
            licence_name__icontains=licence_name
        ).order_by('licence_name'))
    
    @staticmethod
    def get_or_create(licence_name: str, defaults: Optional[dict] = None) -> tuple[Licence, bool]:
        """
        Obtiene o crea una licencia.
        
        Args:
            licence_name: Nombre de la licencia
            defaults: Valores por defecto para crear la licencia
            
        Returns:
            Tupla (licencia, creada)
        """
        # Usar filter().first() para evitar problemas con múltiples objetos
        existing = Licence.objects.filter(licence_name=licence_name).first()
        if existing:
            return existing, False
        
        # Crear nueva licencia
        new_licence = Licence.objects.create(
            licence_name=licence_name,
            **(defaults or {})
        )
        return new_licence, True
    
    @staticmethod
    def update(licence: Licence, **kwargs) -> Licence:
        """
        Actualiza una licencia existente.
        
        Args:
            licence: Instancia de la licencia a actualizar
            **kwargs: Campos a actualizar
            
        Returns:
            Licencia actualizada
        """
        for key, value in kwargs.items():
            setattr(licence, key, value)
        licence.save()
        return licence
    
    @staticmethod
    def delete(licence: Licence) -> bool:
        """
        Elimina una licencia.
        
        Args:
            licence: Instancia de la licencia a eliminar
            
        Returns:
            True si se eliminó correctamente
        """
        licence.delete()
        return True
    
    @staticmethod
    def has_products(licence: Licence) -> bool:
        """
        Verifica si una licencia tiene productos asociados.
        
        Args:
            licence: Instancia de la licencia
            
        Returns:
            True si tiene productos, False en caso contrario
        """
        return Product.objects.filter(licence=licence).exists()
    
    @staticmethod
    def count_products(licence: Licence) -> int:
        """
        Cuenta los productos asociados a una licencia.
        
        Args:
            licence: Instancia de la licencia
            
        Returns:
            Número de productos asociados
        """
        return Product.objects.filter(licence=licence).count()

