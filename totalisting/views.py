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
    """Vista que lista las categorías disponibles en formato JSON."""
    categories_data = CategoryService.get_all_categories()
    return JsonResponse(categories_data, safe=False, json_dumps_params={'ensure_ascii': False, 'indent': 2})

def category_list_by_license(request, license_name):
    """Vista que lista las categorías disponibles filtradas por licencia en formato JSON."""
    categories_data = CategoryService.get_categories_by_licence(license_name)
    return JsonResponse(categories_data, safe=False, json_dumps_params={'ensure_ascii': False, 'indent': 2})

def category(request, category_name):
    """Vista que lista los productos disponibles por categoría."""
    return HttpResponse(f"Listing products in category: {category_name}")

# --- Funciones de lectura de Licencias ---

def license_view(request):
    """Vista que lista todas las licencias disponibles en formato JSON."""
    licenses_data = LicenceService.get_all_licences()
    return JsonResponse(licenses_data, safe=False, json_dumps_params={'ensure_ascii': False, 'indent': 2})

def license(request, license_name):
    """Vista que lista las licencias disponibles filtradas por nombre."""
    licenses_data = LicenceService.get_licences_by_name(license_name)
    return JsonResponse(licenses_data, safe=False, json_dumps_params={'ensure_ascii': False, 'indent': 2})

# --- Funciones de lectura de Productos ---

def product_list(request):
    """Vista que lista todos los productos disponibles."""
    products_data = ProductService.get_all_products()
    return JsonResponse(products_data, safe=False, json_dumps_params={'ensure_ascii': False, 'indent': 2})

def product_list_by_category(request, category_name):
    """Vista que lista todos los productos disponibles por categoría en formato JSON."""
    products_data = ProductService.get_products_by_category(category_name)
    return JsonResponse(products_data, safe=False, json_dumps_params={'ensure_ascii': False, 'indent': 2})

def product_list_by_license(request, license_name):
    """Vista que lista todos los productos disponibles por licencia en formato JSON."""
    products_data = ProductService.get_products_by_licence(license_name)
    return JsonResponse(products_data, safe=False, json_dumps_params={'ensure_ascii': False, 'indent': 2})

def product(request, product_name):
    """Vista que lista el producto seleccionado."""
    return HttpResponse(f"Listing product: {product_name}")

# --- Funciones de búsqueda específica de Productos ---

def find_product_by_id(request, product_id):
    """Busca un producto por su ID en la base de datos."""
    if request.method != 'GET':
        return JsonResponse({'message': 'Método no permitido'}, status=405)
    
    product_data, error_message = ProductService.get_product_by_id(product_id)
    
    if error_message:
        return JsonResponse({'message': error_message}, status=404)
    
    return JsonResponse(product_data, safe=False, json_dumps_params={'ensure_ascii': False, 'indent': 2})

def find_product_by_name(request, product_name):
    """Busca un producto por su nombre en la base de datos."""
    if request.method != 'GET':
        return JsonResponse({'message': 'Método no permitido'}, status=405)
    
    product_data, error_message = ProductService.get_product_by_name(product_name)
    
    if error_message:
        status_code = 400 if 'Múltiples' in error_message else 404
        return JsonResponse({'message': error_message}, status=status_code)
    
    return JsonResponse(product_data, safe=False, json_dumps_params={'ensure_ascii': False, 'indent': 2})

def find_product_by_sku(request, sku):
    """Busca un producto por su SKU en la base de datos."""
    if request.method != 'GET':
        return JsonResponse({'message': 'Método no permitido'}, status=405)
    
    product_data, error_message = ProductService.get_product_by_sku(sku)
    
    if error_message:
        return JsonResponse({'message': error_message}, status=404)
    
    return JsonResponse(product_data, safe=False, json_dumps_params={'ensure_ascii': False, 'indent': 2})


# ============================================================================
# UPDATE - Funciones para actualizar registros
# ============================================================================

@csrf_exempt
def update_product(request, product_id):
    """Actualiza un producto existente en la base de datos con manejo de múltiples imágenes."""
    if request.method not in ['PUT', 'POST']:
        return JsonResponse({'message': 'Método no permitido'}, status=405)
    
    try:
        import json  # Asegurar que json esté disponible en todo el scope de la función
        
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

@csrf_exempt
def update_category(request, category_id):
    """Actualiza una categoría existente en la base de datos."""
    if request.method not in ['PUT', 'POST']:
        return JsonResponse({'message': 'Método no permitido'}, status=405)
    
    # Extraer datos del request
    if hasattr(request, 'data'):
        data = request.data
    else:
        data = dict(request.POST.items())
    
    # Actualizar categoría usando el servicio
    category, error_message = CategoryService.update_category(category_id, data)
    
    if error_message:
        status_code = 404 if 'no encontrada' in error_message.lower() else 500
        return JsonResponse({
            'message': error_message
        }, status=status_code)
    
    return JsonResponse({
        'message': 'Categoría actualizada correctamente',
        'category_id': category.category_id,
        'category_name': category.category_name
    }, status=200, json_dumps_params={'ensure_ascii': False, 'indent': 2})

@csrf_exempt
def update_licence(request, licence_id):
    """Actualiza una licencia existente en la base de datos."""
    if request.method not in ['PUT', 'POST']:
        return JsonResponse({'message': 'Método no permitido'}, status=405)
    
    # Extraer datos del request
    if hasattr(request, 'data'):
        data = request.data
    else:
        data = dict(request.POST.items())
    
    # Actualizar licencia usando el servicio
    licence, error_message = LicenceService.update_licence(licence_id, data)
    
    if error_message:
        status_code = 404 if 'no encontrada' in error_message.lower() else 500
        return JsonResponse({
            'message': error_message
        }, status=status_code)
    
    return JsonResponse({
        'message': 'Licencia actualizada correctamente',
        'licence_id': licence.licence_id,
        'licence_name': licence.licence_name
    }, status=200, json_dumps_params={'ensure_ascii': False, 'indent': 2})


# ============================================================================
# DELETE - Funciones para eliminar registros
# ============================================================================

@csrf_exempt
def delete_product(request, product_id):
    """Elimina un producto de la base de datos."""
    if request.method not in ['DELETE', 'POST']:
        return JsonResponse({'message': 'Método no permitido'}, status=405)
    
    # Eliminar producto usando el servicio
    success, error_message, product_data = ProductService.delete_product(product_id)
    
    if not success:
        status_code = 404 if 'no encontrado' in error_message.lower() else 500
        return JsonResponse({
            'message': error_message
        }, status=status_code)
    
    return JsonResponse({
        'message': 'Producto eliminado correctamente',
        **product_data
    }, status=200, json_dumps_params={'ensure_ascii': False, 'indent': 2})

@csrf_exempt
def delete_category(request, category_id):
    """Elimina una categoría de la base de datos."""
    if request.method not in ['DELETE', 'POST']:
        return JsonResponse({'message': 'Método no permitido'}, status=405)
    
    # Eliminar categoría usando el servicio
    success, error_message, category_data = CategoryService.delete_category(category_id)
    
    if not success:
        status_code = 404 if 'no encontrada' in error_message.lower() else 400
        return JsonResponse({
            'message': error_message,
            **(category_data or {})
        }, status=status_code)
    
    return JsonResponse({
        'message': 'Categoría eliminada correctamente',
        **category_data
    }, status=200, json_dumps_params={'ensure_ascii': False, 'indent': 2})

@csrf_exempt
def delete_licence(request, licence_id):
    """Elimina una licencia de la base de datos."""
    if request.method not in ['DELETE', 'POST']:
        return JsonResponse({'message': 'Método no permitido'}, status=405)
    
    # Eliminar licencia usando el servicio
    success, error_message, licence_data = LicenceService.delete_licence(licence_id)
    
    if not success:
        status_code = 404 if 'no encontrada' in error_message.lower() else 400
        return JsonResponse({
            'message': error_message,
            **(licence_data or {})
        }, status=status_code)
    
    return JsonResponse({
        'message': 'Licencia eliminada correctamente',
        **licence_data
    }, status=200, json_dumps_params={'ensure_ascii': False, 'indent': 2})

