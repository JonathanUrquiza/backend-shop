"""
Factory para crear productos.

Este módulo contiene la clase ProductFactory que encapsula la lógica compleja
de creación de productos, incluyendo el manejo de relaciones (licencia y categoría).

El Factory Pattern se usa aquí para:
- Centralizar la lógica de creación de productos
- Manejar automáticamente la creación de licencias/categorías si no existen
- Validar datos antes de crear
- Retornar metadata sobre qué se creó
"""

# Importar tipos de Python para type hints
from typing import Dict, Any, Optional
# Importar modelos para trabajar con instancias
from ..models import Product, Licence, Category
# Importar repositorios para acceso a datos
from ..repositories.licence_repository import LicenceRepository
from ..repositories.category_repository import CategoryRepository
from ..repositories.product_repository import ProductRepository


class ProductFactory:
    """
    Factory para crear productos.
    
    Esta clase encapsula toda la lógica de creación de productos, incluyendo:
    - Validación de datos
    - Verificación de SKU único
    - Manejo de relaciones (licencia y categoría)
    - Creación automática de licencias/categorías si no existen
    """
    
    @staticmethod
    def create_product(data: Dict[str, Any]) -> tuple[Optional[Product], Optional[str], Dict[str, Any]]:
        """
        Crea un producto con sus relaciones (licencia y categoría).
        
        Este método es el punto central para crear productos. Se encarga de:
        1. Validar los datos recibidos
        2. Verificar que el SKU sea único
        3. Obtener o crear la licencia asociada
        4. Obtener o crear la categoría asociada
        5. Crear el producto en la base de datos
        6. Retornar metadata sobre qué se creó
        
        Si la licencia o categoría no existen, las crea automáticamente con
        valores por defecto. Esto permite crear productos sin necesidad de
        crear primero la licencia/categoría manualmente.
        
        Args:
            data: Diccionario con los datos del producto
                 Debe contener al menos: product_name, product_description, price,
                 stock, sku, y ya sea licence_id/licence_name y category_id/category_name
        
        Returns:
            tuple[Optional[Product], Optional[str], Dict[str, Any]]:
            - Product: Instancia del producto creado, o None si hubo error
            - str: Mensaje de error si hubo problema, o None si fue exitoso
            - Dict: Metadata con información sobre licencia y categoría:
              {
                  'licence': {'id': 1, 'name': 'Star Wars', 'created': False},
                  'category': {'id': 1, 'name': 'Figuras', 'created': True}
              }
              El campo 'created' indica si la licencia/categoría fue creada en esta operación
        """
        # Validar datos usando el serializer
        # El serializer verifica campos obligatorios y tipos de datos
        from ..serializers.product_serializer import ProductSerializer
        is_valid, error_message, validated_data = ProductSerializer.validate_create_data(data)
        
        # Si la validación falla, retornar error inmediatamente
        if not is_valid:
            return None, error_message, {}
        
        # Verificar si el SKU ya existe en la base de datos
        # El SKU debe ser único, no puede haber dos productos con el mismo SKU
        if ProductRepository.sku_exists(validated_data['sku']):
            return None, f"El SKU '{validated_data['sku']}' ya existe en la base de datos", {}
        
        # Obtener licencia por ID o nombre
        # Si se proporciona licence_id, buscar por ID (más eficiente)
        if validated_data.get('licence_id'):
            # Buscar licencia por ID
            licence_obj = LicenceRepository.get_by_id(validated_data['licence_id'])
            if not licence_obj:
                # Si no se encuentra la licencia con ese ID, retornar error
                return None, f'Licencia con ID {validated_data["licence_id"]} no encontrada', {}
            licence_created = False  # La licencia ya existía, no se creó
        else:
            # Si no hay ID, usar el nombre para obtener o crear la licencia
            # get_or_create busca la licencia, y si no existe, la crea automáticamente
            licence_obj, licence_created = LicenceRepository.get_or_create(
                validated_data['licence_name'],  # Nombre de la licencia
                defaults={
                    # Valores por defecto si se crea una nueva licencia
                    'licence_description': data.get('licence_description', f'Licencia {validated_data["licence_name"]}'),
                    'licence_image': data.get('licence_image', '')  # Imagen vacía por defecto
                }
            )
        
        # Obtener categoría por ID o nombre (misma lógica que licencia)
        if validated_data.get('category_id'):
            # Buscar categoría por ID
            category_obj = CategoryRepository.get_by_id(validated_data['category_id'])
            if not category_obj:
                # Si no se encuentra la categoría con ese ID, retornar error
                return None, f'Categoría con ID {validated_data["category_id"]} no encontrada', {}
            category_created = False  # La categoría ya existía, no se creó
        else:
            # Si no hay ID, usar el nombre para obtener o crear la categoría
            category_obj, category_created = CategoryRepository.get_or_create(
                validated_data['category_name'],  # Nombre de la categoría
                defaults={
                    # Valores por defecto si se crea una nueva categoría
                    'category_description': data.get('category_description', f'Categoría {validated_data["category_name"]}'),
                    'image_category': data.get('image_category', '')  # Imagen vacía por defecto
                }
            )
        
        # Crear el producto en la base de datos
        try:
            # Preparar argumentos para crear el producto
            create_kwargs = {
                'product_name': validated_data['product_name'],  # Nombre del producto
                'product_description': validated_data['product_description'],  # Descripción
                'price': validated_data['price'],  # Precio (float)
                'stock': validated_data['stock'],  # Stock (int)
                'discount': validated_data['discount'],  # Descuento (int o None)
                'sku': validated_data['sku'],  # SKU único
                'dues': validated_data['dues'],  # Cuotas (int o None)
                'created_by': validated_data['created_by'],  # ID del usuario creador
                'image_front': validated_data['image_front'],  # Ruta imagen frontal
                'image_back': validated_data['image_back'],  # Ruta imagen reverso
                'licence': licence_obj,  # Objeto Licence (ForeignKey)
                'category': category_obj,  # Objeto Category (ForeignKey)
            }
            
            # Agregar imágenes adicionales si existen
            # Este campo es opcional, solo se agrega si hay valor
            if validated_data.get('additional_images'):
                create_kwargs['additional_images'] = validated_data['additional_images']
            
            # Crear el producto usando el repositorio
            # El repositorio maneja la inserción en la base de datos
            product = ProductRepository.create(**create_kwargs)
            
            # Preparar metadata sobre la operación
            # Esto es útil para saber si se crearon nuevas licencias/categorías
            metadata = {
                'licence': {
                    'id': licence_obj.licence_id,  # ID de la licencia usada
                    'name': licence_obj.licence_name,  # Nombre de la licencia
                    'created': licence_created  # True si se creó en esta operación
                },
                'category': {
                    'id': category_obj.category_id,  # ID de la categoría usada
                    'name': category_obj.category_name,  # Nombre de la categoría
                    'created': category_created  # True si se creó en esta operación
                }
            }
            
            # Retornar producto creado, sin errores, con metadata
            return product, None, metadata
            
        except Exception as e:
            # Si hay error al crear el producto (ej: violación de constraint, error de BD)
            return None, f'Error al crear el producto: {str(e)}', {}

