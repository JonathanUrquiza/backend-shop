"""
Vistas refactorizadas usando Service Layer Pattern.

Las vistas ahora son delgadas y solo se encargan de:
- Recibir requests HTTP
- Extraer datos del request
- Llamar a los servicios correspondientes
- Retornar respuestas JSON
"""

from django.http import HttpResponse, JsonResponse
from .services import ProductService, CategoryService, LicenceService


# ============================================================================
# CREATE - Funciones para crear nuevos registros
# ============================================================================

def new_product_in_DB(request):
    """Crea un nuevo producto en la base de datos."""
    if request.method != 'POST':
        return JsonResponse({'message': 'Método no permitido'}, status=405)
    
    # Extraer datos del request
    data = dict(request.POST.items())
    
    # Crear producto usando el servicio
    product, error_message, metadata = ProductService.create_product(data)
    
    if error_message:
        status_code = 400 if 'Faltan campos' in error_message or 'SKU' in error_message else 500
        return JsonResponse({
            'message': error_message
        }, status=status_code)
    
    # Preparar respuesta
    response_data = {
        'message': 'Producto creado correctamente',
        'product_id': product.product_id,
        'product_name': product.product_name,
        **metadata
    }
    
    return JsonResponse(response_data, status=201, json_dumps_params={'ensure_ascii': False, 'indent': 2})


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

def update_product(request, product_id):
    """Actualiza un producto existente en la base de datos."""
    if request.method not in ['PUT', 'POST']:
        return JsonResponse({'message': 'Método no permitido'}, status=405)
    
    # Extraer datos del request
    if hasattr(request, 'data'):
        data = request.data
    else:
        data = dict(request.POST.items())
    
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

