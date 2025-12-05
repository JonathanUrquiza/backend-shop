"""
Servicio para la lógica de negocio de licencias.

Este módulo contiene la clase LicenceService que implementa la lógica de negocio
relacionada con licencias. Separa la lógica de negocio de las vistas HTTP,
siguiendo el patrón Service Layer.

El servicio actúa como intermediario entre las vistas (que manejan HTTP) y los
repositorios (que manejan acceso a datos), aplicando validaciones y reglas de negocio.
"""

# Importar tipos de Python para type hints
from typing import Dict, Any, Optional, List
# Importar el modelo Licence para trabajar con instancias
from ..models import Licence
# Importar repositorio para acceso a datos
from ..repositories.licence_repository import LicenceRepository
# Importar serializer para convertir modelos a diccionarios
from ..serializers.licence_serializer import LicenceSerializer


class LicenceService:
    """
    Servicio para licencias.
    
    Esta clase contiene la lógica de negocio relacionada con licencias.
    Proporciona métodos estáticos para operaciones CRUD y consultas.
    
    Todos los métodos son estáticos, lo que significa que no se necesita
    instanciar la clase para usarlos.
    """
    
    @staticmethod
    def get_all_licences() -> List[Dict[str, Any]]:
        """
        Obtiene todas las licencias disponibles en el sistema.
        
        Este método retorna todas las licencias serializadas como diccionarios,
        listas para ser enviadas al frontend como JSON.
        
        Returns:
            List[Dict[str, Any]]: Lista de diccionarios con los datos de las licencias
                                Cada diccionario contiene: licence_id, licence_name,
                                licence_description, licence_image
                                Lista vacía si no hay licencias
        
        Ejemplo:
            >>> licences = LicenceService.get_all_licences()
            >>> len(licences)
            8
        """
        # Obtener todas las licencias usando el repositorio
        licences = LicenceRepository.get_all()
        
        # Serializar las licencias a diccionarios usando el serializer
        return LicenceSerializer.to_dict_list(licences)
    
    @staticmethod
    def get_licences_by_name(licence_name: str) -> List[Dict[str, Any]]:
        """
        Obtiene licencias filtradas por nombre (búsqueda parcial).
        
        Este método busca licencias cuyo nombre contenga el texto especificado.
        Es útil para búsquedas y autocompletado en el frontend.
        
        Args:
            licence_name: Nombre de la licencia a buscar (string)
                        Puede ser parcial (ej: "star" encontrará "Star Wars")
        
        Returns:
            List[Dict[str, Any]]: Lista de diccionarios con las licencias que coinciden
                                Lista vacía si no hay coincidencias
            
        Ejemplo:
            >>> licences = LicenceService.get_licences_by_name("star")
            >>> len(licences)
            1  # Encuentra "Star Wars"
        """
        # Obtener licencias filtradas por nombre usando el repositorio
        licences = LicenceRepository.get_by_name(licence_name)
        
        # Serializar las licencias a diccionarios usando el serializer
        return LicenceSerializer.to_dict_list(licences)
    
    @staticmethod
    def create_licence(data: Dict[str, Any]) -> tuple[Optional[Licence], Optional[str]]:
        """
        Crea una nueva licencia en el sistema.
        
        Este método valida los datos, verifica que no exista una licencia con el mismo
        nombre y crea la nueva licencia en la base de datos.
        
        Args:
            data: Diccionario con los datos de la licencia a crear
                 Debe contener al menos 'licence_name'
                 Opcionalmente puede contener 'licence_description' e 'licence_image'
        
        Returns:
            tuple[Optional[Licence], Optional[str]]:
            - Licence: Instancia de la licencia creada, o None si hubo error
            - str: Mensaje de error si hubo problema, o None si fue exitoso
            
        Ejemplo:
            >>> licence, error = LicenceService.create_licence({
            ...     'licence_name': 'Nueva Licencia',
            ...     'licence_description': 'Descripción'
            ... })
            >>> if not error:
            ...     print(licence.licence_id)
            9
        """
        # Extraer el nombre de la licencia (campo obligatorio)
        licence_name = data.get('licence_name')
        
        # Validar que el nombre esté presente
        if not licence_name:
            return None, 'El nombre de la licencia es obligatorio'
        
        # Verificar si ya existe una licencia con ese nombre (evitar duplicados)
        # get_by_name retorna una lista (puede haber múltiples con nombre similar)
        existing_list = LicenceRepository.get_by_name(licence_name)
        if existing_list:
            # Si hay alguna licencia con ese nombre, retornar error
            return None, f'La licencia "{licence_name}" ya existe'
        
        # Crear la licencia usando el repositorio
        try:
            # get_or_create busca la licencia y si no existe la crea
            # [0] obtiene solo el objeto Licence (el segundo elemento es el bool "creada")
            licence = LicenceRepository.get_or_create(
                licence_name,  # Nombre de la licencia
                defaults={
                    # Valores por defecto si se crea una nueva licencia
                    'licence_description': data.get('licence_description', ''),  # Descripción (vacío si no se proporciona)
                    'licence_image': data.get('licence_image', '')  # Ruta de imagen (vacío si no se proporciona)
                }
            )[0]  # Obtener solo el objeto Licence, no el tuple completo
            
            # Retornar la licencia creada sin errores
            return licence, None
        except Exception as e:
            # Si hay error al crear (ej: error de base de datos), retornar error
            return None, f'Error al crear la licencia: {str(e)}'
    
    @staticmethod
    def update_licence(licence_id: int, data: Dict[str, Any]) -> tuple[Optional[Licence], Optional[str]]:
        """
        Actualiza una licencia existente en el sistema.
        
        Este método permite modificar los campos de una licencia existente.
        Solo se actualizan los campos proporcionados en data, los demás permanecen sin cambios.
        
        Args:
            licence_id: ID único de la licencia a actualizar (número entero)
            data: Diccionario con los campos a actualizar
                 Puede contener: 'licence_name', 'licence_description', 'licence_image'
                 Solo se actualizan los campos presentes en el diccionario
        
        Returns:
            tuple[Optional[Licence], Optional[str]]:
            - Licence: Instancia de la licencia actualizada, o None si hubo error
            - str: Mensaje de error si hubo problema, o None si fue exitoso
            
        Ejemplo:
            >>> licence, error = LicenceService.update_licence(1, {
            ...     'licence_description': 'Nueva descripción'
            ... })
            >>> if not error:
            ...     print(licence.licence_description)
            'Nueva descripción'
        """
        # Buscar la licencia por ID usando el repositorio
        licence = LicenceRepository.get_by_id(licence_id)
        
        # Validar que la licencia exista
        if not licence:
            return None, 'Licencia no encontrada'
        
        # Preparar diccionario con solo los campos a actualizar
        update_data = {}
        
        # Agregar campos solo si están presentes en data
        if 'licence_name' in data:
            update_data['licence_name'] = data['licence_name']
        if 'licence_description' in data:
            update_data['licence_description'] = data.get('licence_description', '')
        if 'licence_image' in data:
            update_data['licence_image'] = data.get('licence_image', '')
        
        # Actualizar la licencia usando el repositorio
        try:
            updated_licence = LicenceRepository.update(licence, **update_data)
            return updated_licence, None
        except Exception as e:
            # Si hay error al actualizar (ej: error de base de datos), retornar error
            return None, f'Error al actualizar la licencia: {str(e)}'
    
    @staticmethod
    def delete_licence(licence_id: int) -> tuple[bool, Optional[str], Optional[Dict[str, Any]]]:
        """
        Elimina una licencia del sistema.
        
        Este método valida que la licencia exista y que no tenga productos asociados
        antes de eliminarla. Esto previene eliminar licencias que están en uso.
        
        Args:
            licence_id: ID único de la licencia a eliminar (número entero)
        
        Returns:
            tuple[bool, Optional[str], Optional[Dict[str, Any]]]:
            - bool: True si se eliminó exitosamente, False si hubo error
            - str: Mensaje de error si hubo problema, o None si fue exitoso
            - Dict: Datos de la licencia eliminada (ID y nombre) para referencia
            
        Ejemplo:
            >>> success, error, data = LicenceService.delete_licence(1)
            >>> if success:
            ...     print(f"Eliminada: {data['licence_name']}")
            'Eliminada: Star Wars'
        """
        # Buscar la licencia por ID usando el repositorio
        licence = LicenceRepository.get_by_id(licence_id)
        
        # Validar que la licencia exista
        if not licence:
            return False, 'Licencia no encontrada', None
        
        # Verificar si tiene productos asociados antes de eliminar
        # Esto previene eliminar licencias que están en uso
        products_count = LicenceRepository.count_products(licence)
        
        if products_count > 0:
            # Si tiene productos, no se puede eliminar
            # Retornar información sobre cuántos productos tiene
            return False, f'No se puede eliminar la licencia porque tiene {products_count} producto(s) asociado(s)', {
                'licence_id': licence.licence_id,  # ID de la licencia
                'products_count': products_count  # Número de productos asociados
            }
        
        # Preparar datos de la licencia para retornar después de eliminar
        licence_data = {
            'licence_id': licence.licence_id,  # ID de la licencia eliminada
            'licence_name': licence.licence_name  # Nombre de la licencia eliminada
        }
        
        # Eliminar la licencia usando el repositorio
        try:
            LicenceRepository.delete(licence)
            # Retornar éxito con datos de la licencia eliminada
            return True, None, licence_data
        except Exception as e:
            # Si hay error al eliminar (ej: error de base de datos), retornar error
            return False, f'Error al eliminar la licencia: {str(e)}', None

