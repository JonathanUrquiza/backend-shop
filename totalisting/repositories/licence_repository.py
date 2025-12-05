"""
Repositorio para el modelo Licence.

Este módulo contiene la clase LicenceRepository que abstrae todas las operaciones
de acceso a datos relacionadas con licencias. Implementa el Repository Pattern
que separa la lógica de acceso a datos de la lógica de negocio.

El repositorio proporciona métodos para:
- Obtener licencias (todas, por ID, por nombre)
- Crear licencias (con get_or_create para evitar duplicados)
- Actualizar licencias
- Eliminar licencias
- Verificar relaciones con productos

Todas las consultas a la base de datos relacionadas con licencias deben pasar
por este repositorio, no acceder directamente al modelo Licence.
"""

# Importar tipos de Python para type hints
from typing import Optional, List
# Importar excepciones de Django para manejo de errores de base de datos
from django.core.exceptions import ObjectDoesNotExist
# Importar los modelos Licence y Product para trabajar con instancias
from ..models import Licence, Product


class LicenceRepository:
    """
    Repositorio para licencias.
    
    Esta clase encapsula todas las operaciones de acceso a datos relacionadas
    con licencias. Proporciona una interfaz limpia y consistente para interactuar
    con la tabla 'licence' de la base de datos.
    
    Todos los métodos son estáticos, lo que significa que no se necesita
    instanciar la clase para usarlos.
    """
    
    @staticmethod
    def get_all() -> List[Licence]:
        """
        Obtiene todas las licencias ordenadas por ID.
        
        Este método retorna todas las licencias de la base de datos ordenadas
        por ID. Es útil para listar todas las licencias disponibles en el sistema.
        
        Returns:
            List[Licence]: Lista de todas las licencias ordenadas por ID
                         Lista vacía si no hay licencias
        
        Ejemplo:
            >>> licences = LicenceRepository.get_all()
            >>> len(licences)
            8
        """
        # Obtener todas las licencias usando el ORM de Django
        # .all() obtiene todos los registros
        # .order_by('licence_id') ordena por ID (orden de creación)
        # list() convierte el QuerySet a lista de Python
        return list(Licence.objects.all().order_by('licence_id'))
    
    @staticmethod
    def get_by_id(licence_id: int) -> Optional[Licence]:
        """
        Obtiene una licencia por su ID.
        
        Este método busca una licencia específica usando su ID único.
        Es el método más eficiente para obtener una licencia cuando se conoce su ID.
        
        Args:
            licence_id: ID único de la licencia a buscar (número entero)
            
        Returns:
            Optional[Licence]: Instancia del Licence si existe, None si no se encuentra
            
        Ejemplo:
            >>> licence = LicenceRepository.get_by_id(1)
            >>> if licence:
            ...     print(licence.licence_name)
            'Star Wars'
        """
        try:
            # Usar .get() para obtener un único registro por ID
            # .get() lanza excepción si no encuentra o encuentra múltiples
            return Licence.objects.get(licence_id=licence_id)
        except ObjectDoesNotExist:
            # Si la licencia no existe, retornar None en lugar de lanzar excepción
            # Esto hace el código más robusto y fácil de manejar
            return None
    
    @staticmethod
    def get_by_name(licence_name: str) -> List[Licence]:
        """
        Obtiene licencias filtradas por nombre (búsqueda parcial).
        
        Este método busca licencias cuyo nombre contenga el texto especificado.
        La búsqueda es case-insensitive y parcial, así que "star" encontrará
        "Star Wars", "STAR WARS", etc.
        
        Args:
            licence_name: Nombre de la licencia a buscar (string)
                        Puede ser parcial (ej: "star" encontrará "Star Wars")
            
        Returns:
            List[Licence]: Lista de licencias que coinciden con el nombre,
                          ordenadas alfabéticamente por nombre
                          Lista vacía si no hay coincidencias
            
        Ejemplo:
            >>> licences = LicenceRepository.get_by_name("star")
            >>> len(licences)
            1  # Encuentra "Star Wars"
        """
        # Filtrar licencias por nombre usando búsqueda parcial case-insensitive
        # __icontains: búsqueda case-insensitive parcial (contiene el texto)
        # .order_by('licence_name'): ordenar alfabéticamente
        return list(Licence.objects.filter(
            licence_name__icontains=licence_name
        ).order_by('licence_name'))
    
    @staticmethod
    def get_or_create(licence_name: str, defaults: Optional[dict] = None) -> tuple[Licence, bool]:
        """
        Obtiene o crea una licencia.
        
        Este método busca una licencia por nombre, y si no existe, la crea.
        Es útil para evitar duplicados y crear licencias automáticamente cuando
        se necesita (ej: al crear un producto con una licencia nueva).
        
        Args:
            licence_name: Nombre de la licencia a buscar o crear (string)
            defaults: Diccionario con valores por defecto para crear la licencia
                     (ej: {'licence_description': '...', 'licence_image': '...'})
            
        Returns:
            tuple[Licence, bool]: 
            - Licence: Instancia de la licencia (existente o recién creada)
            - bool: True si se creó, False si ya existía
            
        Ejemplo:
            >>> licence, created = LicenceRepository.get_or_create(
            ...     "Nueva Licencia",
            ...     defaults={'licence_description': 'Descripción'}
            ... )
            >>> created
            True  # Se creó nueva
        """
        # Usar filter().first() para evitar problemas con múltiples objetos
        # Buscar licencia existente por nombre exacto
        existing = Licence.objects.filter(licence_name=licence_name).first()
        
        if existing:
            # Si existe, retornar la licencia existente y False (no se creó)
            return existing, False
        
        # Si no existe, crear nueva licencia
        # Usar defaults si se proporcionaron, sino usar diccionario vacío
        new_licence = Licence.objects.create(
            licence_name=licence_name,  # Nombre de la licencia (obligatorio)
            **(defaults or {})  # Desempaquetar valores por defecto si existen
        )
        
        # Retornar la licencia creada y True (se creó)
        return new_licence, True
    
    @staticmethod
    def update(licence: Licence, **kwargs) -> Licence:
        """
        Actualiza una licencia existente en la base de datos.
        
        Este método modifica los campos especificados de una licencia existente.
        Solo se actualizan los campos proporcionados en kwargs, los demás
        permanecen sin cambios.
        
        Args:
            licence: Instancia del Licence a actualizar (debe existir en la BD)
            **kwargs: Campos a actualizar con sus nuevos valores
                    Solo se actualizan los campos proporcionados
                    Ejemplo: {'licence_description': 'Nueva descripción'}
            
        Returns:
            Licence: Instancia del Licence actualizada (la misma instancia)
            
        Ejemplo:
            >>> licence = LicenceRepository.get_by_id(1)
            >>> updated = LicenceRepository.update(licence, licence_description='Nueva desc')
            >>> updated.licence_description
            'Nueva desc'
        """
        # Iterar sobre todos los campos a actualizar
        for key, value in kwargs.items():
            # Usar setattr para asignar el nuevo valor al campo
            # Esto es equivalente a: licence.key = value
            setattr(licence, key, value)
        
        # Guardar los cambios en la base de datos
        # .save() actualiza el registro existente
        licence.save()
        
        # Retornar la instancia actualizada
        return licence
    
    @staticmethod
    def delete(licence: Licence) -> bool:
        """
        Elimina una licencia de la base de datos.
        
        Este método elimina permanentemente el registro de la licencia de la
        base de datos. La operación no se puede deshacer.
        
        IMPORTANTE: No elimina los productos asociados, solo el registro de la licencia.
        Los productos quedarán sin licencia (o con licencia NULL dependiendo de la BD).
        
        Args:
            licence: Instancia del Licence a eliminar (debe existir en la BD)
            
        Returns:
            bool: Siempre retorna True si no hay error
                 (si hay error, lanza excepción)
            
        Ejemplo:
            >>> licence = LicenceRepository.get_by_id(1)
            >>> LicenceRepository.delete(licence)
            True
        """
        # Eliminar la licencia de la base de datos
        # .delete() elimina el registro permanentemente
        licence.delete()
        
        # Retornar True para indicar éxito
        return True
    
    @staticmethod
    def has_products(licence: Licence) -> bool:
        """
        Verifica si una licencia tiene productos asociados.
        
        Este método es útil para validar antes de eliminar una licencia,
        ya que normalmente no se debería eliminar una licencia que tiene productos.
        
        Args:
            licence: Instancia del Licence a verificar
            
        Returns:
            bool: True si tiene al menos un producto asociado, False si no tiene productos
            
        Ejemplo:
            >>> licence = LicenceRepository.get_by_id(1)
            >>> LicenceRepository.has_products(licence)
            True
        """
        # Verificar si existe al menos un producto con esta licencia
        # .exists() es más eficiente que .count() > 0 porque se detiene al encontrar el primero
        return Product.objects.filter(licence=licence).exists()
    
    @staticmethod
    def count_products(licence: Licence) -> int:
        """
        Cuenta los productos asociados a una licencia.
        
        Este método cuenta cuántos productos pertenecen a una licencia específica.
        Útil para mostrar estadísticas o validar antes de eliminar.
        
        Args:
            licence: Instancia del Licence a contar
            
        Returns:
            int: Número de productos asociados a esta licencia
                0 si no tiene productos
            
        Ejemplo:
            >>> licence = LicenceRepository.get_by_id(1)
            >>> LicenceRepository.count_products(licence)
            12
        """
        # Contar productos que tienen esta licencia asociada
        # .count() retorna el número total de productos
        return Product.objects.filter(licence=licence).count()

