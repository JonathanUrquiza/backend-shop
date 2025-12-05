"""
Vistas refactorizadas usando Service Layer Pattern.

Las vistas ahora son delgadas y solo se encargan de:
- Recibir requests HTTP
- Extraer datos del request
- Llamar a los servicios correspondientes
- Retornar respuestas JSON
"""

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .services import ProductService, CategoryService, LicenceService
from .utils.file_utils import save_category_image, save_licence_image, save_product_images
import json


# ============================================================================
# CREATE - Funciones para crear nuevos registros
# ============================================================================

@csrf_exempt
def create_category(request):
    """Crea una nueva categoría con imagen."""
    if request.method != 'POST':
        return JsonResponse({'message': 'Método no permitido'}, status=405)
    
    try:
        category_name = request.POST.get('category_name')
        category_description = request.POST.get('category_description', '')
        image_file = request.FILES.get('image_category')
        
        if not category_name:
            return JsonResponse({'message': 'El nombre de la categoría es obligatorio'}, status=400)
        
        # Guardar imagen si se proporcionó
        image_path = None
        if image_file:
            image_path = save_category_image(image_file, category_name)
            if not image_path:
                return JsonResponse({'message': 'Error al guardar la imagen'}, status=500)
        
        # Crear categoría usando el servicio
        data = {
            'category_name': category_name,
            'category_description': category_description,
            'image_category': image_path
        }
        
        category, error_message = CategoryService.create_category(data)
        
        if error_message:
            return JsonResponse({'message': error_message}, status=400)
        
        return JsonResponse({
            'message': 'Categoría creada correctamente',
            'category_id': category.category_id,
            'category_name': category.category_name,
            'image_category': category.image_category
        }, status=201)
        
    except Exception as e:
        return JsonResponse({'message': f'Error al crear categoría: {str(e)}'}, status=500)


@csrf_exempt
def create_licence(request):
    """Crea una nueva licencia con imagen."""
    if request.method != 'POST':
        return JsonResponse({'message': 'Método no permitido'}, status=405)
    
    try:
        licence_name = request.POST.get('licence_name')
        licence_description = request.POST.get('licence_description', '')
        image_file = request.FILES.get('licence_image')
        
        if not licence_name:
            return JsonResponse({'message': 'El nombre de la licencia es obligatorio'}, status=400)
        
        # Guardar imagen si se proporcionó
        image_path = None
        if image_file:
            image_path = save_licence_image(image_file, licence_name)
            if not image_path:
                return JsonResponse({'message': 'Error al guardar la imagen'}, status=500)
        
        # Crear licencia usando el servicio
        data = {
            'licence_name': licence_name,
            'licence_description': licence_description,
            'licence_image': image_path
        }
        
        licence, error_message = LicenceService.create_licence(data)
        
        if error_message:
            return JsonResponse({'message': error_message}, status=400)
        
        return JsonResponse({
            'message': 'Licencia creada correctamente',
            'licence_id': licence.licence_id,
            'licence_name': licence.licence_name,
            'licence_image': licence.licence_image
        }, status=201)
        
    except Exception as e:
        return JsonResponse({'message': f'Error al crear licencia: {str(e)}'}, status=500)


@csrf_exempt
def new_product_in_DB(request):
    """Crea un nuevo producto en la base de datos con manejo de múltiples imágenes."""
    if request.method != 'POST':
        return JsonResponse({'message': 'Método no permitido'}, status=405)
    
    try:
        # Manejar form-data con archivos
        if request.FILES:
            # Extraer datos del formulario
            data = dict(request.POST.items())
            
            # Obtener imágenes
            front_image = request.FILES.get('image_front')
            back_image = request.FILES.get('image_back')
            additional_images = []
            
            # Obtener todas las imágenes adicionales (pueden venir como image_additional_0, image_additional_1, etc.)
            idx = 0
            while f'image_additional_{idx}' in request.FILES:
                additional_images.append(request.FILES.get(f'image_additional_{idx}'))
                idx += 1
            
            # Si no hay imágenes con índice, buscar image_additional como lista
            if not additional_images and 'image_additional' in request.FILES:
                files = request.FILES.getlist('image_additional')
                additional_images.extend(files)
            
            # Obtener licencia y categoría (deben existir)
            licence_id = data.get('licence_id')
            category_id = data.get('category_id')
            product_name = data.get('product_name')
            
            if not licence_id or not category_id:
                return JsonResponse({'message': 'Debe seleccionar una licencia y una categoría'}, status=400)
            
            # Obtener nombres de licencia y categoría para crear carpetas
            from .models import Licence, Category
            licence = Licence.objects.filter(licence_id=licence_id).first()
            category = Category.objects.filter(category_id=category_id).first()
            
            if not licence or not category:
                return JsonResponse({'message': 'Licencia o categoría no encontrada'}, status=404)
            
            # Guardar imágenes en la estructura de carpetas
            image_paths = save_product_images(
                front_image=front_image,
                back_image=back_image,
                additional_images=additional_images,
                licence_name=licence.licence_name,
                product_name=product_name or 'product'
            )
            
            # Agregar rutas de imágenes a los datos
            data['image_front'] = image_paths.get('image_front', '')
            data['image_back'] = image_paths.get('image_back', '')
            
            # Guardar imágenes adicionales como JSON
            if image_paths.get('additional_images'):
                data['additional_images'] = json.dumps(image_paths['additional_images'])
            
            # Agregar nombres de licencia y categoría para el servicio
            data['licence_name'] = licence.licence_name
            data['category_name'] = category.category_name
            
        else:
            # Manejar JSON (sin archivos, solo rutas)
            if request.content_type == 'application/json':
                try:
                    data = json.loads(request.body)
                except json.JSONDecodeError:
                    return JsonResponse({'message': 'JSON inválido'}, status=400)
            else:
                data = dict(request.POST.items())
        
        # Crear producto usando el servicio
        product, error_message, metadata = ProductService.create_product(data)
        
        if error_message:
            status_code = 400 if 'Faltan campos' in error_message or 'SKU' in error_message else 500
            import traceback
            print(f"Error al crear producto: {error_message}")
            print(f"Datos recibidos: {data}")
            print(f"Traceback: {traceback.format_exc()}")
            return JsonResponse({
                'message': error_message,
                'error_details': str(error_message) if status_code == 500 else None
            }, status=status_code)
        
        # Preparar respuesta
        response_data = {
            'message': 'Producto creado correctamente',
            'product_id': product.product_id,
            'product_name': product.product_name,
            **metadata
        }
        
        return JsonResponse(response_data, status=201, json_dumps_params={'ensure_ascii': False, 'indent': 2})
        
    except Exception as e:
        return JsonResponse({'message': f'Error al crear producto: {str(e)}'}, status=500)


# ============================================================================
# READ - Funciones para leer/consultar registros
# ============================================================================

# --- Funciones de lectura de Categorías ---

def listing(request):
    """
    Endpoint para listar todas las categorías disponibles.
    
    Endpoint: GET /category/
    
    Retorna:
    - 200: Lista de todas las categorías en formato JSON
    - 500: Error del servidor
    
    Ejemplo de respuesta:
    [
        {
            "category_id": 1,
            "category_name": "Figuras",
            "category_description": "...",
            "image_category": "/categories/figuras.webp"
        },
        ...
    ]
    """
    # Obtener todas las categorías usando el servicio
    categories_data = CategoryService.get_all_categories()
    
    # Retornar respuesta JSON con formato legible
    # safe=False permite retornar arrays directamente
    # ensure_ascii=False permite caracteres especiales (tildes, etc.)
    # indent=2 formatea el JSON con indentación para legibilidad
    return JsonResponse(categories_data, safe=False, json_dumps_params={'ensure_ascii': False, 'indent': 2})

def category_list_by_license(request, license_name):
    """
    Endpoint para listar categorías filtradas por licencia.
    
    Endpoint: GET /category/by-license/<license_name>/
    
    Parámetros:
    - license_name: Nombre de la licencia (viene en la URL)
    
    Retorna:
    - 200: Lista de categorías que tienen productos de esa licencia en formato JSON
    - 500: Error del servidor
    
    Ejemplo:
    GET /category/by-license/star-wars/
    Retorna todas las categorías que tienen productos de Star Wars
    """
    # Obtener categorías filtradas por licencia usando el servicio
    categories_data = CategoryService.get_categories_by_licence(license_name)
    
    # Retornar respuesta JSON con formato legible
    return JsonResponse(categories_data, safe=False, json_dumps_params={'ensure_ascii': False, 'indent': 2})

def category(request, category_name):
    """
    Endpoint placeholder para obtener información de una categoría específica.
    
    Endpoint: GET /category/<category_name>/
    
    NOTA: Esta función actualmente solo retorna un mensaje de texto.
    Debería implementarse para retornar información detallada de la categoría.
    
    Parámetros:
    - category_name: Nombre de la categoría (viene en la URL)
    
    Retorna:
    - 200: Mensaje de texto (debería ser JSON con datos de la categoría)
    """
    # TODO: Implementar lógica para retornar datos de la categoría en formato JSON
    return HttpResponse(f"Listing products in category: {category_name}")

# --- Funciones de lectura de Licencias ---

def license_view(request):
    """
    Endpoint para listar todas las licencias disponibles.
    
    Endpoint: GET /licence/
    
    Retorna:
    - 200: Lista de todas las licencias en formato JSON
    - 500: Error del servidor
    
    Ejemplo de respuesta:
    [
        {
            "licence_id": 1,
            "licence_name": "Star Wars",
            "licence_description": "...",
            "licence_image": "/licences/star-wars.webp"
        },
        ...
    ]
    """
    # Obtener todas las licencias usando el servicio
    licenses_data = LicenceService.get_all_licences()
    
    # Retornar respuesta JSON con formato legible
    return JsonResponse(licenses_data, safe=False, json_dumps_params={'ensure_ascii': False, 'indent': 2})

def license(request, license_name):
    """
    Endpoint para buscar licencias por nombre (búsqueda parcial).
    
    Endpoint: GET /licence/<license_name>/
    
    Parámetros:
    - license_name: Nombre de la licencia a buscar (viene en la URL, búsqueda parcial)
    
    Retorna:
    - 200: Lista de licencias que coinciden con el nombre en formato JSON
    - 500: Error del servidor
    
    Ejemplo:
    GET /licence/star/
    Retorna todas las licencias que contengan "star" en el nombre (case-insensitive)
    """
    # Obtener licencias filtradas por nombre usando el servicio
    licenses_data = LicenceService.get_licences_by_name(license_name)
    
    # Retornar respuesta JSON con formato legible
    return JsonResponse(licenses_data, safe=False, json_dumps_params={'ensure_ascii': False, 'indent': 2})

# --- Funciones de lectura de Productos ---

def product_list(request):
    """
    Endpoint para listar todos los productos disponibles.
    
    Endpoint: GET /product/list/
    
    Esta es una de las rutas más usadas del backend, ya que el frontend
    carga todos los productos al iniciar para mostrar el catálogo.
    
    Retorna:
    - 200: Lista de todos los productos en formato JSON
    - 500: Error del servidor
    
    Ejemplo de respuesta:
    [
        {
            "product_id": 1,
            "product_name": "Baby Yoda Blueball",
            "price": 5200.99,
            "stock": 10,
            ...
        },
        ...
    ]
    """
    # Obtener todos los productos usando el servicio
    products_data = ProductService.get_all_products()
    
    # Retornar respuesta JSON con formato legible
    return JsonResponse(products_data, safe=False, json_dumps_params={'ensure_ascii': False, 'indent': 2})

def product_list_by_category(request, category_name):
    """
    Endpoint para listar productos filtrados por categoría.
    
    Endpoint: GET /product/list/category/<category_name>/
    
    Parámetros:
    - category_name: Nombre de la categoría (viene en la URL, búsqueda parcial)
    
    Retorna:
    - 200: Lista de productos de esa categoría en formato JSON
    - 500: Error del servidor
    
    Ejemplo:
    GET /product/list/category/figuras/
    Retorna todos los productos que pertenecen a la categoría "Figuras"
    """
    # Obtener productos filtrados por categoría usando el servicio
    products_data = ProductService.get_products_by_category(category_name)
    
    # Retornar respuesta JSON con formato legible
    return JsonResponse(products_data, safe=False, json_dumps_params={'ensure_ascii': False, 'indent': 2})

def product_list_by_license(request, license_name):
    """
    Endpoint para listar productos filtrados por licencia.
    
    Endpoint: GET /product/list/license/<license_name>/
    
    Parámetros:
    - license_name: Nombre de la licencia (viene en la URL, búsqueda parcial)
    
    Retorna:
    - 200: Lista de productos de esa licencia en formato JSON
    - 500: Error del servidor
    
    Ejemplo:
    GET /product/list/license/star-wars/
    Retorna todos los productos que pertenecen a la licencia "Star Wars"
    """
    # Obtener productos filtrados por licencia usando el servicio
    products_data = ProductService.get_products_by_licence(license_name)
    
    # Retornar respuesta JSON con formato legible
    return JsonResponse(products_data, safe=False, json_dumps_params={'ensure_ascii': False, 'indent': 2})

def product(request, product_name):
    """
    Endpoint placeholder para obtener información de un producto específico por nombre.
    
    Endpoint: GET /product/<product_name>/
    
    NOTA: Esta función actualmente solo retorna un mensaje de texto.
    Debería implementarse para retornar información detallada del producto.
    Para buscar productos, usar find_product_by_id o find_product_by_name.
    
    Parámetros:
    - product_name: Nombre del producto (viene en la URL)
    
    Retorna:
    - 200: Mensaje de texto (debería ser JSON con datos del producto)
    """
    # TODO: Implementar lógica para retornar datos del producto en formato JSON
    return HttpResponse(f"Listing product: {product_name}")

# --- Funciones de búsqueda específica de Productos ---

def find_product_by_id(request, product_id):
    """
    Endpoint para buscar un producto por su ID único.
    
    Endpoint: GET /product/find/id/<product_id>/
    
    Esta es la forma más eficiente y precisa de obtener un producto específico.
    
    Parámetros:
    - product_id: ID único del producto (viene en la URL como número entero)
    
    Retorna:
    - 200: Datos del producto en formato JSON (incluye relaciones con licencia y categoría)
    - 404: Producto no encontrado
    - 405: Método HTTP no permitido
    
    Ejemplo:
    GET /product/find/id/1/
    Retorna el producto con ID 1 con toda su información completa
    """
    # Validar que el método HTTP sea GET
    if request.method != 'GET':
        return JsonResponse({'message': 'Método no permitido'}, status=405)
    
    # Buscar el producto por ID usando el servicio
    product_data, error_message = ProductService.get_product_by_id(product_id)
    
    # Si hay error (producto no encontrado), retornar error 404
    if error_message:
        return JsonResponse({'message': error_message}, status=404)
    
    # Retornar datos del producto en formato JSON con formato legible
    return JsonResponse(product_data, safe=False, json_dumps_params={'ensure_ascii': False, 'indent': 2})

def find_product_by_name(request, product_name):
    """
    Endpoint para buscar un producto por su nombre exacto.
    
    Endpoint: GET /product/find/name/<product_name>/
    
    Parámetros:
    - product_name: Nombre exacto del producto (viene en la URL)
    
    Retorna:
    - 200: Datos del producto en formato JSON
    - 400: Múltiples productos con el mismo nombre (no debería pasar)
    - 404: Producto no encontrado
    - 405: Método HTTP no permitido
    
    Ejemplo:
    GET /product/find/name/baby-yoda-blueball/
    Retorna el producto con ese nombre exacto
    """
    # Validar que el método HTTP sea GET
    if request.method != 'GET':
        return JsonResponse({'message': 'Método no permitido'}, status=405)
    
    # Buscar el producto por nombre usando el servicio
    product_data, error_message = ProductService.get_product_by_name(product_name)
    
    # Si hay error, determinar el código de estado apropiado
    if error_message:
        # Si hay múltiples productos con el mismo nombre, retornar error 400
        # Si no se encuentra, retornar error 404
        status_code = 400 if 'Múltiples' in error_message else 404
        return JsonResponse({'message': error_message}, status=status_code)
    
    # Retornar datos del producto en formato JSON con formato legible
    return JsonResponse(product_data, safe=False, json_dumps_params={'ensure_ascii': False, 'indent': 2})

def find_product_by_sku(request, sku):
    """
    Endpoint para buscar un producto por su SKU (código único).
    
    Endpoint: GET /product/find/sku/<sku>/
    
    El SKU es un código único que identifica cada producto, útil para búsquedas
    desde códigos de barras o referencias externas.
    
    Parámetros:
    - sku: SKU del producto (viene en la URL como string)
    
    Retorna:
    - 200: Datos del producto en formato JSON
    - 404: Producto no encontrado
    - 405: Método HTTP no permitido
    
    Ejemplo:
    GET /product/find/sku/STW001001/
    Retorna el producto con ese SKU exacto
    """
    # Validar que el método HTTP sea GET
    if request.method != 'GET':
        return JsonResponse({'message': 'Método no permitido'}, status=405)
    
    # Buscar el producto por SKU usando el servicio
    product_data, error_message = ProductService.get_product_by_sku(sku)
    
    # Si hay error (producto no encontrado), retornar error 404
    if error_message:
        return JsonResponse({'message': error_message}, status=404)
    
    # Retornar datos del producto en formato JSON con formato legible
    return JsonResponse(product_data, safe=False, json_dumps_params={'ensure_ascii': False, 'indent': 2})


# ============================================================================
# UPDATE - Funciones para actualizar registros
# ============================================================================

@csrf_exempt  # Deshabilitar protección CSRF para este endpoint de API
def update_product(request, product_id):
    """
    Actualiza un producto existente en la base de datos con manejo de múltiples imágenes.
    
    Endpoint: POST /product/update/<product_id>/
    
    Esta función permite actualizar un producto existente, incluyendo:
    - Datos básicos del producto (nombre, descripción, precio, stock, etc.)
    - Imágenes (frontal, reverso, adicionales)
    - Licencia y categoría
    
    Características especiales:
    - Si se sube una nueva imagen frontal, se actualiza; si no, se mantiene la existente
    - Si se suben nuevas imágenes adicionales, se combinan con las existentes
    - Preserva todas las imágenes existentes cuando no se proporcionan nuevas
    
    Parámetros:
    - request: Objeto HTTP request de Django
    - product_id: ID del producto a actualizar (viene en la URL)
    
    Retorna:
    - 200: Producto actualizado exitosamente
    - 400: Error de validación
    - 404: Producto, licencia o categoría no encontrada
    - 405: Método HTTP no permitido
    - 500: Error del servidor
    """
    # Validar que el método HTTP sea POST o PUT (ambos permitidos para actualizar)
    if request.method not in ['PUT', 'POST']:
        return JsonResponse({'message': 'Método no permitido'}, status=405)
    
    try:
        # Importar json al inicio de la función para asegurar disponibilidad en todo el scope
        import json  # Asegurar que json esté disponible en todo el scope de la función
        
        # Manejar form-data con archivos (cuando se suben nuevas imágenes)
        if request.FILES:  # Si hay archivos en el request
            # Extraer datos del formulario
            data = dict(request.POST.items())
            
            # Obtener imágenes
            front_image = request.FILES.get('image_front')
            back_image = request.FILES.get('image_back')
            additional_images = []
            
            # Obtener todas las imágenes adicionales (pueden venir como image_additional_0, image_additional_1, etc.)
            idx = 0
            while f'image_additional_{idx}' in request.FILES:
                additional_images.append(request.FILES.get(f'image_additional_{idx}'))
                idx += 1
            
            # Si no hay imágenes con índice, buscar image_additional como lista
            if not additional_images and 'image_additional' in request.FILES:
                files = request.FILES.getlist('image_additional')
                additional_images.extend(files)
            
            # Obtener licencia y categoría si se proporcionan
            licence_id = data.get('licence_id')
            category_id = data.get('category_id')
            product_name = data.get('product_name')
            
            # Obtener producto existente para mantener datos si no se proporcionan nuevos
            from .models import Product, Licence, Category
            existing_product = Product.objects.filter(product_id=product_id).first()
            
            if not existing_product:
                return JsonResponse({'message': 'Producto no encontrado'}, status=404)
            
            # Si se proporcionan nuevas imágenes, guardarlas
            if front_image or back_image or additional_images:
                # Obtener nombres de licencia y categoría (del producto existente o de los nuevos datos)
                if licence_id:
                    licence = Licence.objects.filter(licence_id=licence_id).first()
                else:
                    licence = existing_product.licence
                
                if category_id:
                    category = Category.objects.filter(category_id=category_id).first()
                else:
                    category = existing_product.category
                
                if not licence or not category:
                    return JsonResponse({'message': 'Licencia o categoría no encontrada'}, status=404)
                
                # Guardar imágenes en la estructura de carpetas
                image_paths = save_product_images(
                    front_image=front_image,
                    back_image=back_image,
                    additional_images=additional_images,
                    licence_name=licence.licence_name,
                    product_name=product_name or existing_product.product_name
                )
                
                # Agregar rutas de imágenes a los datos (solo si se proporcionaron nuevas imágenes)
                # Si no se proporciona una nueva imagen, mantener la existente
                if image_paths.get('image_front'):
                    data['image_front'] = image_paths['image_front']
                elif not front_image:
                    # Mantener la imagen frontal existente si no se proporciona una nueva
                    data['image_front'] = existing_product.image_front or ''
                
                if image_paths.get('image_back'):
                    data['image_back'] = image_paths['image_back']
                elif not back_image:
                    # Mantener la imagen reverso existente si no se proporciona una nueva
                    data['image_back'] = existing_product.image_back or ''
                
                # Guardar imágenes adicionales como JSON
                if image_paths.get('additional_images'):
                    # Si hay nuevas imágenes adicionales, combinarlas con las existentes
                    existing_additional = []
                    if existing_product.additional_images:
                        try:
                            existing_additional = json.loads(existing_product.additional_images) if isinstance(existing_product.additional_images, str) else existing_product.additional_images
                        except:
                            existing_additional = []
                    
                    # Combinar imágenes existentes con las nuevas
                    combined_additional = existing_additional + image_paths['additional_images']
                    data['additional_images'] = json.dumps(combined_additional)
                elif not additional_images:
                    # Mantener las imágenes adicionales existentes si no se proporcionan nuevas
                    if existing_product.additional_images:
                        data['additional_images'] = existing_product.additional_images if isinstance(existing_product.additional_images, str) else json.dumps(existing_product.additional_images)
            
            # Agregar nombres de licencia y categoría si se proporcionaron IDs
            if licence_id:
                licence = Licence.objects.filter(licence_id=licence_id).first()
                if licence:
                    data['licence_name'] = licence.licence_name
            if category_id:
                category = Category.objects.filter(category_id=category_id).first()
                if category:
                    data['category_name'] = category.category_name
        else:
            # Manejar JSON (sin archivos, solo rutas)
            if hasattr(request, 'data'):
                data = request.data
            elif request.content_type == 'application/json':
                try:
                    data = json.loads(request.body)
                except json.JSONDecodeError:
                    return JsonResponse({'message': 'JSON inválido'}, status=400)
            else:
                data = dict(request.POST.items())
            
            # Si no hay archivos, mantener las imágenes existentes
            from .models import Product
            existing_product = Product.objects.filter(product_id=product_id).first()
            if existing_product:
                if 'image_front' not in data:
                    data['image_front'] = existing_product.image_front or ''
                if 'image_back' not in data:
                    data['image_back'] = existing_product.image_back or ''
                if 'additional_images' not in data and existing_product.additional_images:
                    data['additional_images'] = existing_product.additional_images if isinstance(existing_product.additional_images, str) else json.dumps(existing_product.additional_images)
        
        # Actualizar producto usando el servicio
        product, error_message = ProductService.update_product(product_id, data)
        
        if error_message:
            status_code = 404 if 'no encontrado' in error_message.lower() else 400
            return JsonResponse({
                'message': error_message
            }, status=status_code)
        
        return JsonResponse({
            'message': 'Producto actualizado correctamente',
            'product_id': product.product_id,
            'product_name': product.product_name
        }, status=200, json_dumps_params={'ensure_ascii': False, 'indent': 2})
    
    except Exception as e:
        return JsonResponse({'message': f'Error al actualizar producto: {str(e)}'}, status=500)

@csrf_exempt  # Deshabilitar protección CSRF para este endpoint de API
def update_category(request, category_id):
    """
    Actualiza una categoría existente en la base de datos.
    
    Endpoint: POST/PUT /category/update/<category_id>/
    
    Parámetros esperados (JSON o form-data):
    - category_name (opcional): Nuevo nombre de la categoría
    - category_description (opcional): Nueva descripción
    - image_category (opcional): Nueva ruta de imagen
    
    Retorna:
    - 200: Categoría actualizada exitosamente
    - 404: Categoría no encontrada
    - 405: Método HTTP no permitido
    - 500: Error del servidor
    """
    # Validar que el método HTTP sea POST o PUT (ambos permitidos para actualizar)
    if request.method not in ['PUT', 'POST']:
        return JsonResponse({'message': 'Método no permitido'}, status=405)
    
    # Extraer datos del request
    # Verificar si el request tiene atributo 'data' (usado por algunos frameworks)
    if hasattr(request, 'data'):
        data = request.data
    else:
        # Si no tiene 'data', extraer datos del formulario POST
        data = dict(request.POST.items())
    
    # Actualizar categoría usando el servicio
    # El servicio maneja la validación y lógica de negocio
    category, error_message = CategoryService.update_category(category_id, data)
    
    # Si hay error, determinar el código de estado apropiado
    if error_message:
        # Si el error indica que no se encontró la categoría, usar 404
        # Si es otro error, usar 500 (error del servidor)
        status_code = 404 if 'no encontrada' in error_message.lower() else 500
        return JsonResponse({
            'message': error_message
        }, status=status_code)
    
    # Retornar respuesta exitosa con datos de la categoría actualizada
    return JsonResponse({
        'message': 'Categoría actualizada correctamente',
        'category_id': category.category_id,  # ID de la categoría actualizada
        'category_name': category.category_name  # Nombre de la categoría actualizada
    }, status=200, json_dumps_params={'ensure_ascii': False, 'indent': 2})

@csrf_exempt  # Deshabilitar protección CSRF para este endpoint de API
def update_licence(request, licence_id):
    """
    Actualiza una licencia existente en la base de datos.
    
    Endpoint: POST/PUT /licence/update/<licence_id>/
    
    Parámetros esperados (JSON o form-data):
    - licence_name (opcional): Nuevo nombre de la licencia
    - licence_description (opcional): Nueva descripción
    - licence_image (opcional): Nueva ruta de imagen
    
    Retorna:
    - 200: Licencia actualizada exitosamente
    - 404: Licencia no encontrada
    - 405: Método HTTP no permitido
    - 500: Error del servidor
    """
    # Validar que el método HTTP sea POST o PUT (ambos permitidos para actualizar)
    if request.method not in ['PUT', 'POST']:
        return JsonResponse({'message': 'Método no permitido'}, status=405)
    
    # Extraer datos del request
    # Verificar si el request tiene atributo 'data' (usado por algunos frameworks)
    if hasattr(request, 'data'):
        data = request.data
    else:
        # Si no tiene 'data', extraer datos del formulario POST
        data = dict(request.POST.items())
    
    # Actualizar licencia usando el servicio
    # El servicio maneja la validación y lógica de negocio
    licence, error_message = LicenceService.update_licence(licence_id, data)
    
    # Si hay error, determinar el código de estado apropiado
    if error_message:
        # Si el error indica que no se encontró la licencia, usar 404
        # Si es otro error, usar 500 (error del servidor)
        status_code = 404 if 'no encontrada' in error_message.lower() else 500
        return JsonResponse({
            'message': error_message
        }, status=status_code)
    
    # Retornar respuesta exitosa con datos de la licencia actualizada
    return JsonResponse({
        'message': 'Licencia actualizada correctamente',
        'licence_id': licence.licence_id,  # ID de la licencia actualizada
        'licence_name': licence.licence_name  # Nombre de la licencia actualizada
    }, status=200, json_dumps_params={'ensure_ascii': False, 'indent': 2})


# ============================================================================
# DELETE - Funciones para eliminar registros
# ============================================================================

@csrf_exempt  # Deshabilitar protección CSRF para este endpoint de API
def delete_product(request, product_id):
    """
    Elimina un producto de la base de datos.
    
    Endpoint: DELETE /product/delete/<product_id>/
    
    Esta función elimina permanentemente un producto del sistema.
    La operación no se puede deshacer.
    
    IMPORTANTE: No elimina las imágenes del sistema de archivos, solo
    el registro de la base de datos.
    
    Parámetros:
    - request: Objeto HTTP request de Django
    - product_id: ID del producto a eliminar (viene en la URL)
    
    Retorna:
    - 200: Producto eliminado exitosamente con datos del producto eliminado
    - 404: Producto no encontrado
    - 405: Método HTTP no permitido
    - 500: Error del servidor
    """
    # Validar que el método HTTP sea DELETE o POST (ambos permitidos para eliminar)
    if request.method not in ['DELETE', 'POST']:
        return JsonResponse({'message': 'Método no permitido'}, status=405)
    
    # Eliminar producto usando el servicio
    # El servicio retorna: (success, error_message, product_data)
    success, error_message, product_data = ProductService.delete_product(product_id)
    
    # Si no fue exitoso, determinar el código de estado apropiado
    if not success:
        # Si el error indica que no se encontró el producto, usar 404
        # Si es otro error, usar 500 (error del servidor)
        status_code = 404 if 'no encontrado' in error_message.lower() else 500
        return JsonResponse({
            'message': error_message
        }, status=status_code)
    
    # Retornar respuesta exitosa con datos del producto eliminado
    # **product_data desempaqueta el diccionario con datos del producto
    return JsonResponse({
        'message': 'Producto eliminado correctamente',
        **product_data  # Incluir product_id y product_name del producto eliminado
    }, status=200, json_dumps_params={'ensure_ascii': False, 'indent': 2})

@csrf_exempt  # Deshabilitar protección CSRF para este endpoint de API
def delete_category(request, category_id):
    """
    Elimina una categoría de la base de datos.
    
    Endpoint: DELETE /category/delete/<category_id>/
    
    Esta función elimina permanentemente una categoría del sistema.
    La operación no se puede deshacer.
    
    IMPORTANTE: No se puede eliminar una categoría que tiene productos asociados.
    El servicio valida esto antes de eliminar.
    
    Parámetros:
    - request: Objeto HTTP request de Django
    - category_id: ID de la categoría a eliminar (viene en la URL)
    
    Retorna:
    - 200: Categoría eliminada exitosamente con datos de la categoría eliminada
    - 400: No se puede eliminar porque tiene productos asociados
    - 404: Categoría no encontrada
    - 405: Método HTTP no permitido
    """
    # Validar que el método HTTP sea DELETE o POST (ambos permitidos para eliminar)
    if request.method not in ['DELETE', 'POST']:
        return JsonResponse({'message': 'Método no permitido'}, status=405)
    
    # Eliminar categoría usando el servicio
    # El servicio valida que no tenga productos asociados antes de eliminar
    success, error_message, category_data = CategoryService.delete_category(category_id)
    
    # Si no fue exitoso, determinar el código de estado apropiado
    if not success:
        # Si el error indica que no se encontró la categoría, usar 404
        # Si indica que tiene productos asociados, usar 400 (Bad Request)
        status_code = 404 if 'no encontrada' in error_message.lower() else 400
        return JsonResponse({
            'message': error_message,
            **(category_data or {})  # Incluir datos de la categoría si están disponibles
        }, status=status_code)
    
    # Retornar respuesta exitosa con datos de la categoría eliminada
    return JsonResponse({
        'message': 'Categoría eliminada correctamente',
        **category_data  # Incluir category_id y category_name de la categoría eliminada
    }, status=200, json_dumps_params={'ensure_ascii': False, 'indent': 2})

@csrf_exempt  # Deshabilitar protección CSRF para este endpoint de API
def delete_licence(request, licence_id):
    """
    Elimina una licencia de la base de datos.
    
    Endpoint: DELETE /licence/delete/<licence_id>/
    
    Esta función elimina permanentemente una licencia del sistema.
    La operación no se puede deshacer.
    
    IMPORTANTE: No se puede eliminar una licencia que tiene productos asociados.
    El servicio valida esto antes de eliminar.
    
    Parámetros:
    - request: Objeto HTTP request de Django
    - licence_id: ID de la licencia a eliminar (viene en la URL)
    
    Retorna:
    - 200: Licencia eliminada exitosamente con datos de la licencia eliminada
    - 400: No se puede eliminar porque tiene productos asociados
    - 404: Licencia no encontrada
    - 405: Método HTTP no permitido
    """
    # Validar que el método HTTP sea DELETE o POST (ambos permitidos para eliminar)
    if request.method not in ['DELETE', 'POST']:
        return JsonResponse({'message': 'Método no permitido'}, status=405)
    
    # Eliminar licencia usando el servicio
    # El servicio valida que no tenga productos asociados antes de eliminar
    success, error_message, licence_data = LicenceService.delete_licence(licence_id)
    
    # Si no fue exitoso, determinar el código de estado apropiado
    if not success:
        # Si el error indica que no se encontró la licencia, usar 404
        # Si indica que tiene productos asociados, usar 400 (Bad Request)
        status_code = 404 if 'no encontrada' in error_message.lower() else 400
        return JsonResponse({
            'message': error_message,
            **(licence_data or {})  # Incluir datos de la licencia si están disponibles
        }, status=status_code)
    
    # Retornar respuesta exitosa con datos de la licencia eliminada
    return JsonResponse({
        'message': 'Licencia eliminada correctamente',
        **licence_data  # Incluir licence_id y licence_name de la licencia eliminada
    }, status=200, json_dumps_params={'ensure_ascii': False, 'indent': 2})

