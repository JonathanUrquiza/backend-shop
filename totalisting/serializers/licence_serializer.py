"""
Serializer para el modelo Licence.

Este módulo contiene la clase LicenceSerializer que se encarga de convertir
objetos Licence (modelos Django) a diccionarios JSON que pueden ser enviados
al frontend.

El serializer actúa como una capa de transformación entre los modelos de Django
y las representaciones JSON que se envían al frontend.
"""

# Importar tipos de Python para type hints
from typing import Dict, Any
# Importar el modelo Licence para trabajar con instancias
from ..models import Licence


class LicenceSerializer:
    """
    Serializer para licencias.
    
    Esta clase proporciona métodos estáticos para convertir objetos Licence
    (modelos Django) a diccionarios JSON.
    
    Los métodos principales son:
    - to_dict: Convierte un Licence a diccionario
    - to_dict_list: Convierte una lista de Licences a lista de diccionarios
    """
    
    @staticmethod
    def to_dict(licence: Licence) -> Dict[str, Any]:
        """
        Convierte un objeto Licence a diccionario JSON.
        
        Este método serializa un objeto Licence de Django a un diccionario Python
        que puede ser fácilmente convertido a JSON para enviar al frontend.
        
        Args:
            licence: Instancia del modelo Licence a serializar
            
        Returns:
            Dict[str, Any]: Diccionario con los datos de la licencia en formato JSON-friendly
            
        Ejemplo de retorno:
        {
            'licence_id': 1,
            'licence_name': 'Star Wars',
            'licence_description': 'Licencia de Star Wars',
            'licence_image': '/licences/star-wars.webp'
        }
        """
        return {
            'licence_id': licence.licence_id,  # ID único de la licencia
            'licence_name': licence.licence_name,  # Nombre de la licencia
            'licence_description': licence.licence_description or '',  # Descripción (vacío si None)
            'licence_image': licence.licence_image or '',  # Ruta de la imagen (vacío si None)
        }
    
    @staticmethod
    def to_dict_list(licences) -> list:
        """
        Convierte una lista de licencias a lista de diccionarios JSON.
        
        Este método es útil para serializar múltiples licencias a la vez,
        como cuando se lista todas las licencias disponibles.
        
        Args:
            licences: QuerySet de Django o lista de objetos Licence
                    Puede ser el resultado de Licence.objects.all() o cualquier filtro
            
        Returns:
            list: Lista de diccionarios, cada uno representando una licencia
            
        Ejemplo:
            >>> licences = Licence.objects.all()
            >>> LicenceSerializer.to_dict_list(licences)
            [{'licence_id': 1, 'licence_name': '...', ...}, ...]
        """
        # Usar list comprehension para convertir cada licencia a diccionario
        # Esto es más eficiente que un loop explícito
        return [LicenceSerializer.to_dict(licence) for licence in licences]

