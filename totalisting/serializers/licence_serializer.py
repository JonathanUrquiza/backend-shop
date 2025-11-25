"""
Serializer para el modelo Licence.

Convierte objetos Licence a diccionarios JSON.
"""

from typing import Dict, Any
from ..models import Licence


class LicenceSerializer:
    """Serializer para licencias."""
    
    @staticmethod
    def to_dict(licence: Licence) -> Dict[str, Any]:
        """
        Convierte un objeto Licence a diccionario.
        
        Args:
            licence: Instancia del modelo Licence
            
        Returns:
            Diccionario con los datos de la licencia
        """
        return {
            'licence_id': licence.licence_id,
            'licence_name': licence.licence_name,
            'licence_description': licence.licence_description or '',
            'licence_image': licence.licence_image or '',
        }
    
    @staticmethod
    def to_dict_list(licences) -> list:
        """
        Convierte una lista de licencias a lista de diccionarios.
        
        Args:
            licences: QuerySet o lista de licencias
            
        Returns:
            Lista de diccionarios con los datos de las licencias
        """
        return [LicenceSerializer.to_dict(licence) for licence in licences]

