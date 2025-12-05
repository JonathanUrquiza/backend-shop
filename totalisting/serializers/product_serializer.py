"""
Serializer para el modelo Product.

Este módulo contiene la clase ProductSerializer que se encarga de:
- Convertir objetos Product (modelos Django) a diccionarios JSON
- Validar datos para crear productos
- Manejar la serialización de campos complejos como additional_images

El serializer actúa como una capa de transformación entre los modelos de Django
y las representaciones JSON que se envían al frontend.
"""

# Importar tipos de Python para type hints
from typing import Dict, Any, Optional
# Importar módulo json para serializar/deserializar datos JSON
import json
# Importar el modelo Product para trabajar con instancias
from ..models import Product


def _parse_additional_images(value) -> Optional[str]:
    """
    Parsea y normaliza el campo additional_images que puede venir en diferentes formatos.
    
    Esta función auxiliar maneja la conversión del campo additional_images que puede
    estar almacenado como JSON string en la base de datos o venir como lista/dict
    desde el frontend. Normaliza todo a JSON string para almacenamiento consistente.
    
    Args:
        value: Valor que puede ser:
               - String JSON: '["/path1", "/path2"]'
               - Lista Python: ["/path1", "/path2"]
               - Diccionario Python: {"images": [...]}
               - None o string vacío
               - Cualquier otro tipo
    
    Returns:
        Optional[str]: String JSON válido con el array de imágenes o None si no hay valor
        
    Ejemplos:
        >>> _parse_additional_images('["/img1.webp", "/img2.webp"]')
        '["/img1.webp", "/img2.webp"]'
        >>> _parse_additional_images(["/img1.webp", "/img2.webp"])
        '["/img1.webp", "/img2.webp"]'
        >>> _parse_additional_images(None)
        None
    """
    # Si el valor es None, vacío o falsy, retornar None
    if not value:
        return None
    
    # Si el valor es un string, verificar si es JSON válido
    if isinstance(value, str):
        try:
            # Intentar parsear el string como JSON
            parsed = json.loads(value)
            # Si se puede parsear y tiene contenido, convertir de vuelta a JSON string
            # Esto normaliza el formato y valida que sea JSON válido
            return json.dumps(parsed) if parsed else None
        except (json.JSONDecodeError, TypeError):
            # Si no es JSON válido o hay error de tipo, retornar None
            # Esto maneja casos donde el string no es JSON válido
            return None
    
    # Si el valor es una lista o diccionario de Python
    if isinstance(value, (list, dict)):
        # Convertir a JSON string si tiene contenido
        # json.dumps convierte el objeto Python a string JSON
        return json.dumps(value) if value else None
    
    # Si no coincide con ningún tipo esperado, retornar None
    return None


class ProductSerializer:
    """
    Serializer para productos.
    
    Esta clase proporciona métodos estáticos para convertir objetos Product
    (modelos Django) a diccionarios JSON y validar datos para crear productos.
    
    Los métodos principales son:
    - to_dict: Convierte un Product a diccionario
    - to_dict_list: Convierte una lista de Products a lista de diccionarios
    - validate_create_data: Valida y normaliza datos para crear un producto
    """
    
    @staticmethod
    def to_dict(product: Product, include_relations: bool = True) -> Dict[str, Any]:
        """
        Convierte un objeto Product a diccionario JSON.
        
        Este método serializa un objeto Product de Django a un diccionario Python
        que puede ser fácilmente convertido a JSON para enviar al frontend.
        
        Args:
            product: Instancia del modelo Product a serializar
            include_relations: Si True, incluye información de licencia y categoría
                             Si False, solo incluye datos básicos del producto
                             (útil para listas donde no se necesita la relación completa)
            
        Returns:
            Dict[str, Any]: Diccionario con los datos del producto en formato JSON-friendly
            
        Ejemplo de retorno:
        {
            'product_id': 1,
            'product_name': 'Baby Yoda Blueball',
            'product_description': '...',
            'price': 5200.99,
            'stock': 10,
            'discount': 10,
            'sku': 'STW001001',
            'image_front': '/star-wars/baby-yoda-1.webp',
            'image_back': '/star-wars/baby-yoda-box.webp',
            'additional_images': ['/star-wars/baby-yoda-2.webp'],
            'licence': {'licence_id': 1, 'licence_name': 'Star Wars'},
            'category': {'category_id': 1, 'category_name': 'Figuras'}
        }
        """
        # Crear diccionario base con los campos principales del producto
        data = {
            'product_id': product.product_id,  # ID único del producto
            'product_name': product.product_name,  # Nombre del producto
            'product_description': product.product_description,  # Descripción del producto
            'price': float(product.price),  # Precio convertido a float (puede ser Decimal)
            'stock': product.stock,  # Cantidad en stock
            'discount': product.discount or 0,  # Descuento (0 si es None)
            'sku': product.sku,  # SKU único del producto
            'image_front': product.image_front or '',  # Ruta imagen frontal (vacío si None)
            'image_back': product.image_back or '',  # Ruta imagen reverso (vacío si None)
        }
        
        # Agregar imágenes adicionales si existen
        # Verificar que el producto tenga el atributo additional_images
        if hasattr(product, 'additional_images') and product.additional_images:
            try:
                import json
                # Parsear el JSON string almacenado en la BD a lista de Python
                # additional_images se almacena como JSON string en la BD
                data['additional_images'] = json.loads(product.additional_images)
            except:
                # Si hay error al parsear (JSON inválido), usar lista vacía
                data['additional_images'] = []
        
        # Si se solicita incluir relaciones, agregar información de licencia y categoría
        if include_relations:
            # Agregar información de la licencia si existe
            if hasattr(product, 'licence') and product.licence:
                data['licence'] = {
                    'licence_id': product.licence.licence_id,  # ID de la licencia
                    'licence_name': product.licence.licence_name,  # Nombre de la licencia
                }
            
            # Agregar información de la categoría si existe
            if hasattr(product, 'category') and product.category:
                data['category'] = {
                    'category_id': product.category.category_id,  # ID de la categoría
                    'category_name': product.category.category_name,  # Nombre de la categoría
                }
        
        return data
    
    @staticmethod
    def to_dict_list(products, include_relations: bool = False) -> list:
        """
        Convierte una lista de productos a lista de diccionarios.
        
        Este método es útil para serializar múltiples productos a la vez,
        como cuando se lista todos los productos o se filtran por categoría/licencia.
        
        Args:
            products: QuerySet de Django o lista de objetos Product
                     Puede ser el resultado de Product.objects.all() o cualquier filtro
            include_relations: Si True, incluye información de licencia y categoría
                             Por defecto False para optimizar cuando no se necesitan relaciones
                             (útil en listas grandes donde solo se muestran datos básicos)
            
        Returns:
            list: Lista de diccionarios, cada uno representando un producto
            
        Ejemplo:
            >>> products = Product.objects.all()
            >>> ProductSerializer.to_dict_list(products)
            [{'product_id': 1, 'product_name': '...', ...}, ...]
        """
        # Usar list comprehension para convertir cada producto a diccionario
        # Esto es más eficiente que un loop explícito
        return [ProductSerializer.to_dict(product, include_relations) for product in products]
    
    @staticmethod
    def validate_create_data(data: Dict[str, Any]) -> tuple[bool, Optional[str], Dict[str, Any]]:
        """
        Valida y normaliza los datos para crear un producto.
        
        Este método valida que todos los campos requeridos estén presentes,
        verifica los tipos de datos y normaliza los valores (convierte strings a números,
        maneja licencia/categoría por ID o nombre, etc.).
        
        Args:
            data: Diccionario con los datos del producto a validar
                 Puede contener campos como:
                 - product_name, product_description, price, stock, sku (obligatorios)
                 - licence_id o licence_name (al menos uno requerido)
                 - category_id o category_name (al menos uno requerido)
                 - discount, dues, image_front, image_back, additional_images (opcionales)
                 - created_by (opcional, default 1)
            
        Returns:
            tuple[bool, Optional[str], Dict[str, Any]]: 
            - bool: True si los datos son válidos, False si hay errores
            - Optional[str]: Mensaje de error si hay problemas, None si es válido
            - Dict[str, Any]: Datos validados y normalizados listos para crear el producto
            
        Ejemplo de uso:
            >>> data = {'product_name': 'Test', 'price': '100', ...}
            >>> is_valid, error, validated = ProductSerializer.validate_create_data(data)
            >>> if is_valid:
            ...     # Usar validated para crear el producto
        """
        # Definir campos obligatorios para crear un producto
        required_fields = ['product_name', 'product_description', 'price', 'stock', 'sku', 'licence', 'category']
        
        # Verificar que todos los campos obligatorios estén presentes
        # Permite que licence/category vengan como 'licence' o 'licence_name'
        missing_fields = [field for field in required_fields 
                         if not data.get(field) and not data.get(f'{field}_name')]
        
        # Si faltan campos obligatorios, retornar error
        if missing_fields:
            return False, f'Faltan campos obligatorios: {", ".join(missing_fields)}', {}
        
        # Validar y convertir tipos de datos
        try:
            # Manejar licencia y categoría por ID o nombre (flexibilidad en la API)
            # Si viene licence_id, usarlo; si no, usar licence_name
            licence_id = data.get('licence_id')
            category_id = data.get('category_id')
            licence_name = data.get('licence') or data.get('licence_name')
            category_name = data.get('category') or data.get('category_name')
            
            # Crear diccionario con datos validados y normalizados
            validated_data = {
                'product_name': str(data.get('product_name', '')),  # Asegurar que sea string
                'product_description': str(data.get('product_description', '')),  # Asegurar que sea string
                'price': float(data.get('price', 0)),  # Convertir a float (puede venir como string)
                'stock': int(data.get('stock', 0)),  # Convertir a int (puede venir como string)
                'discount': int(data.get('discount', 0)) if data.get('discount') else None,  # Int o None
                'sku': str(data.get('sku', '')),  # Asegurar que sea string
                'licence_id': int(licence_id) if licence_id else None,  # Convertir ID a int o None
                'licence_name': licence_name,  # Nombre de la licencia (si no hay ID)
                'category_id': int(category_id) if category_id else None,  # Convertir ID a int o None
                'category_name': category_name,  # Nombre de la categoría (si no hay ID)
                'image_front': data.get('image_front', ''),  # Ruta imagen frontal (string)
                'image_back': data.get('image_back', ''),  # Ruta imagen reverso (string)
                'additional_images': _parse_additional_images(data.get('additional_images', '')),  # Parsear JSON
                'created_by': int(data.get('created_by', 1)),  # ID del usuario creador (default 1)
                'dues': int(data.get('dues')) if data.get('dues') else None,  # Cuotas (int o None)
            }
            # Retornar éxito con datos validados
            return True, None, validated_data
        except (ValueError, TypeError) as e:
            # Si hay error al convertir tipos (ej: "abc" a int), retornar error
            return False, f'Error en los tipos de datos: {str(e)}', {}

