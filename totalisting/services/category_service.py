"""
Servicio para la lógica de negocio de categorías.

Este módulo contiene la clase CategoryService que implementa la lógica de negocio
relacionada con categorías. Separa la lógica de negocio de las vistas HTTP,
siguiendo el patrón Service Layer.

El servicio actúa como intermediario entre las vistas (que manejan HTTP) y los
repositorios (que manejan acceso a datos), aplicando validaciones y reglas de negocio.
"""

# Importar tipos de Python para type hints
from typing import Dict, Any, Optional, List
# Importar el modelo Category para trabajar con instancias
from ..models import Category
# Importar repositorio para acceso a datos
from ..repositories.category_repository import CategoryRepository
# Importar serializer para convertir modelos a diccionarios
from ..serializers.category_serializer import CategorySerializer


class CategoryService:
    """
    Servicio para categorías.
    
    Esta clase contiene la lógica de negocio relacionada con categorías.
    Proporciona métodos estáticos para operaciones CRUD y consultas.
    
    Todos los métodos son estáticos, lo que significa que no se necesita
    instanciar la clase para usarlos.
    """
    
    @staticmethod
    def get_all_categories() -> List[Dict[str, Any]]:
        """
        Obtiene todas las categorías disponibles en el sistema.
        
        Este método retorna todas las categorías serializadas como diccionarios,
        listas para ser enviadas al frontend como JSON.
        
        Returns:
            List[Dict[str, Any]]: Lista de diccionarios con los datos de las categorías
                                 Cada diccionario contiene: category_id, category_name,
                                 category_description, image_category
                                 Lista vacía si no hay categorías
        
        Ejemplo:
            >>> categories = CategoryService.get_all_categories()
            >>> len(categories)
            5
        """
        # Obtener todas las categorías usando el repositorio
        categories = CategoryRepository.get_all()
        
        # Serializar las categorías a diccionarios usando el serializer
        return CategorySerializer.to_dict_list(categories)
    
    @staticmethod
    def get_categories_by_licence(licence_name: str) -> List[Dict[str, Any]]:
        """
        Obtiene categorías que tienen productos de una licencia específica.
        
        Este método es útil para filtrar categorías cuando se selecciona una licencia,
        mostrando solo las categorías que tienen productos disponibles de esa licencia.
        
        Args:
            licence_name: Nombre de la licencia a filtrar (string)
                        Puede ser parcial (ej: "star" encontrará "Star Wars")
            
        Returns:
            List[Dict[str, Any]]: Lista de diccionarios con las categorías que tienen
                                 productos de esa licencia
                                 Lista vacía si no hay categorías con productos de esa licencia
            
        Ejemplo:
            >>> categories = CategoryService.get_categories_by_licence("Star Wars")
            >>> len(categories)
            3
        """
        # Obtener categorías filtradas por licencia usando el repositorio
        categories = CategoryRepository.get_by_licence(licence_name)
        
        # Serializar las categorías a diccionarios usando el serializer
        return CategorySerializer.to_dict_list(categories)
    
    @staticmethod
    def create_category(data: Dict[str, Any]) -> tuple[Optional[Category], Optional[str]]:
        """
        Crea una nueva categoría en el sistema.
        
        Este método valida los datos, verifica que no exista una categoría con el mismo
        nombre y crea la nueva categoría en la base de datos.
        
        Args:
            data: Diccionario con los datos de la categoría a crear
                 Debe contener al menos 'category_name'
                 Opcionalmente puede contener 'category_description' e 'image_category'
        
        Returns:
            tuple[Optional[Category], Optional[str]]:
            - Category: Instancia de la categoría creada, o None si hubo error
            - str: Mensaje de error si hubo problema, o None si fue exitoso
            
        Ejemplo:
            >>> category, error = CategoryService.create_category({
            ...     'category_name': 'Nueva Categoría',
            ...     'category_description': 'Descripción'
            ... })
            >>> if not error:
            ...     print(category.category_id)
            6
        """
        # Extraer el nombre de la categoría (campo obligatorio)
        category_name = data.get('category_name')
        
        # Validar que el nombre esté presente
        if not category_name:
            return None, 'El nombre de la categoría es obligatorio'
        
        # Verificar si ya existe una categoría con ese nombre (evitar duplicados)
        existing = CategoryRepository.get_by_name(category_name)
        if existing:
            return None, f'La categoría "{category_name}" ya existe'
        
        # Crear la categoría usando el repositorio
        try:
            # get_or_create busca la categoría y si no existe la crea
            # [0] obtiene solo el objeto Category (el segundo elemento es el bool "creada")
            category = CategoryRepository.get_or_create(
                category_name,  # Nombre de la categoría
                defaults={
                    # Valores por defecto si se crea una nueva categoría
                    'category_description': data.get('category_description', ''),  # Descripción (vacío si no se proporciona)
                    'image_category': data.get('image_category', '')  # Ruta de imagen (vacío si no se proporciona)
                }
            )[0]  # Obtener solo el objeto Category, no el tuple completo
            
            # Retornar la categoría creada sin errores
            return category, None
        except Exception as e:
            # Si hay error al crear (ej: error de base de datos), retornar error
            return None, f'Error al crear la categoría: {str(e)}'
    
    @staticmethod
    def update_category(category_id: int, data: Dict[str, Any]) -> tuple[Optional[Category], Optional[str]]:
        """
        Actualiza una categoría existente en el sistema.
        
        Este método permite modificar los campos de una categoría existente.
        Solo se actualizan los campos proporcionados en data, los demás permanecen sin cambios.
        
        Args:
            category_id: ID único de la categoría a actualizar (número entero)
            data: Diccionario con los campos a actualizar
                 Puede contener: 'category_name', 'category_description', 'image_category'
                 Solo se actualizan los campos presentes en el diccionario
        
        Returns:
            tuple[Optional[Category], Optional[str]]:
            - Category: Instancia de la categoría actualizada, o None si hubo error
            - str: Mensaje de error si hubo problema, o None si fue exitoso
            
        Ejemplo:
            >>> category, error = CategoryService.update_category(1, {
            ...     'category_description': 'Nueva descripción'
            ... })
            >>> if not error:
            ...     print(category.category_description)
            'Nueva descripción'
        """
        # Buscar la categoría por ID usando el repositorio
        category = CategoryRepository.get_by_id(category_id)
        
        # Validar que la categoría exista
        if not category:
            return None, 'Categoría no encontrada'
        
        # Preparar diccionario con solo los campos a actualizar
        update_data = {}
        
        # Agregar campos solo si están presentes en data
        if 'category_name' in data:
            update_data['category_name'] = data['category_name']
        if 'category_description' in data:
            update_data['category_description'] = data.get('category_description', '')
        if 'image_category' in data:
            update_data['image_category'] = data.get('image_category', '')
        
        # Actualizar la categoría usando el repositorio
        try:
            updated_category = CategoryRepository.update(category, **update_data)
            return updated_category, None
        except Exception as e:
            # Si hay error al actualizar (ej: error de base de datos), retornar error
            return None, f'Error al actualizar la categoría: {str(e)}'
    
    @staticmethod
    def delete_category(category_id: int) -> tuple[bool, Optional[str], Optional[Dict[str, Any]]]:
        """
        Elimina una categoría del sistema.
        
        Este método valida que la categoría exista y que no tenga productos asociados
        antes de eliminarla. Esto previene eliminar categorías que están en uso.
        
        Args:
            category_id: ID único de la categoría a eliminar (número entero)
        
        Returns:
            tuple[bool, Optional[str], Optional[Dict[str, Any]]]:
            - bool: True si se eliminó exitosamente, False si hubo error
            - str: Mensaje de error si hubo problema, o None si fue exitoso
            - Dict: Datos de la categoría eliminada (ID y nombre) para referencia
            
        Ejemplo:
            >>> success, error, data = CategoryService.delete_category(1)
            >>> if success:
            ...     print(f"Eliminada: {data['category_name']}")
            'Eliminada: Figuras'
        """
        # Buscar la categoría por ID usando el repositorio
        category = CategoryRepository.get_by_id(category_id)
        
        # Validar que la categoría exista
        if not category:
            return False, 'Categoría no encontrada', None
        
        # Verificar si tiene productos asociados antes de eliminar
        # Esto previene eliminar categorías que están en uso
        products_count = CategoryRepository.count_products(category)
        
        if products_count > 0:
            # Si tiene productos, no se puede eliminar
            # Retornar información sobre cuántos productos tiene
            return False, f'No se puede eliminar la categoría porque tiene {products_count} producto(s) asociado(s)', {
                'category_id': category.category_id,  # ID de la categoría
                'products_count': products_count  # Número de productos asociados
            }
        
        # Preparar datos de la categoría para retornar después de eliminar
        category_data = {
            'category_id': category.category_id,  # ID de la categoría eliminada
            'category_name': category.category_name  # Nombre de la categoría eliminada
        }
        
        # Eliminar la categoría usando el repositorio
        try:
            CategoryRepository.delete(category)
            # Retornar éxito con datos de la categoría eliminada
            return True, None, category_data
        except Exception as e:
            # Si hay error al eliminar (ej: error de base de datos), retornar error
            return False, f'Error al eliminar la categoría: {str(e)}', None

