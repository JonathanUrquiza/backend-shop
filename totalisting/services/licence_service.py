"""
Servicio para la lógica de negocio de licencias.

Separa la lógica de negocio de las vistas HTTP.
"""

from typing import Dict, Any, Optional, List
from ..models import Licence
from ..repositories.licence_repository import LicenceRepository
from ..serializers.licence_serializer import LicenceSerializer


class LicenceService:
    """Servicio para licencias."""
    
    @staticmethod
    def get_all_licences() -> List[Dict[str, Any]]:
        """
        Obtiene todas las licencias.
        
        Returns:
            Lista de diccionarios con los datos de las licencias
        """
        licences = LicenceRepository.get_all()
        return LicenceSerializer.to_dict_list(licences)
    
    @staticmethod
    def get_licences_by_name(licence_name: str) -> List[Dict[str, Any]]:
        """
        Obtiene licencias filtradas por nombre.
        
        Args:
            licence_name: Nombre de la licencia
            
        Returns:
            Lista de diccionarios con los datos de las licencias
        """
        licences = LicenceRepository.get_by_name(licence_name)
        return LicenceSerializer.to_dict_list(licences)
    
    @staticmethod
    def update_licence(licence_id: int, data: Dict[str, Any]) -> tuple[Optional[Licence], Optional[str]]:
        """
        Actualiza una licencia existente.
        
        Args:
            licence_id: ID de la licencia a actualizar
            data: Diccionario con los campos a actualizar
            
        Returns:
            Tupla (licencia_actualizada, mensaje_error)
        """
        licence = LicenceRepository.get_by_id(licence_id)
        if not licence:
            return None, 'Licencia no encontrada'
        
        update_data = {}
        if 'licence_name' in data:
            update_data['licence_name'] = data['licence_name']
        if 'licence_description' in data:
            update_data['licence_description'] = data.get('licence_description', '')
        if 'licence_image' in data:
            update_data['licence_image'] = data.get('licence_image', '')
        
        try:
            updated_licence = LicenceRepository.update(licence, **update_data)
            return updated_licence, None
        except Exception as e:
            return None, f'Error al actualizar la licencia: {str(e)}'
    
    @staticmethod
    def delete_licence(licence_id: int) -> tuple[bool, Optional[str], Optional[Dict[str, Any]]]:
        """
        Elimina una licencia.
        
        Args:
            licence_id: ID de la licencia a eliminar
            
        Returns:
            Tupla (exito, mensaje_error, datos_de_la_licencia_eliminada)
        """
        licence = LicenceRepository.get_by_id(licence_id)
        if not licence:
            return False, 'Licencia no encontrada', None
        
        # Verificar si tiene productos asociados
        products_count = LicenceRepository.count_products(licence)
        if products_count > 0:
            return False, f'No se puede eliminar la licencia porque tiene {products_count} producto(s) asociado(s)', {
                'licence_id': licence.licence_id,
                'products_count': products_count
            }
        
        licence_data = {
            'licence_id': licence.licence_id,
            'licence_name': licence.licence_name
        }
        
        try:
            LicenceRepository.delete(licence)
            return True, None, licence_data
        except Exception as e:
            return False, f'Error al eliminar la licencia: {str(e)}', None

