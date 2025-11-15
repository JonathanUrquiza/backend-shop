from django.http import HttpResponse, JsonResponse
from .models import Category, Product, Licence

# ============================================================================
# CREATE - Funciones para crear nuevos registros
# ============================================================================

def new_product_in_DB(request):
    """Crea un nuevo producto en la base de datos.
    
    Si la licencia o categoría no existen, las crea automáticamente.
    Relaciona el producto con la licencia y categoría correspondientes.
    """
    if request.method == 'POST':
        try:
            # Obtener datos del producto
            product_name = request.POST.get('product_name')
            product_description = request.POST.get('product_description')
            price = request.POST.get('price')
            stock = request.POST.get('stock')
            discount = request.POST.get('discount')
            sku = request.POST.get('sku')
            licence_name = request.POST.get('licence') or request.POST.get('licence_name')
            category_name = request.POST.get('category') or request.POST.get('category_name')
            image_front = request.POST.get('image_front', '')
            image_back = request.POST.get('image_back', '')
            created_by = request.POST.get('created_by', 1)  # Valor por defecto si no se proporciona
            
            # Validar campos obligatorios
            if not all([product_name, product_description, price, stock, sku, licence_name, category_name]):
                return JsonResponse({
                    'message': 'Faltan campos obligatorios',
                    'required': ['product_name', 'product_description', 'price', 'stock', 'sku', 'licence', 'category']
                }, status=400)
            
            # 1. Obtener o crear la licencia
            licence_obj, licence_created = Licence.objects.get_or_create(
                licence_name=licence_name,
                defaults={
                    'licence_description': request.POST.get('licence_description', f'Licencia {licence_name}'),
                    'licence_image': request.POST.get('licence_image', '')
                }
            )
            
            # 2. Obtener o crear la categoría
            category_obj, category_created = Category.objects.get_or_create(
                category_name=category_name,
                defaults={
                    'category_description': request.POST.get('category_description', f'Categoría {category_name}')
                }
            )
            
            # 3. Verificar si el SKU ya existe
            if Product.objects.filter(sku=sku).exists():
                return JsonResponse({
                    'message': 'El SKU ya existe en la base de datos',
                    'sku': sku
                }, status=400)
            
            # 4. Crear el producto con las relaciones correctas
            product = Product.objects.create(
                product_name=product_name,
                product_description=product_description,
                price=float(price),
                stock=int(stock),
                discount=int(discount) if discount else None,
                sku=sku,
                licence=licence_obj,  # Relación con la licencia
                category=category_obj,  # Relación con la categoría
                image_front=image_front,
                image_back=image_back,
                created_by=int(created_by),
                dues=int(request.POST.get('dues')) if request.POST.get('dues') else None,
            )
            
            # Preparar mensaje de respuesta
            response_data = {
                'message': 'Producto creado correctamente',
                'product_id': product.product_id,
                'product_name': product.product_name,
                'licence': {
                    'id': licence_obj.licence_id,
                    'name': licence_obj.licence_name,
                    'created': licence_created
                },
                'category': {
                    'id': category_obj.category_id,
                    'name': category_obj.category_name,
                    'created': category_created
                }
            }
            
            return JsonResponse(response_data, status=201)
            
        except ValueError as e:
            return JsonResponse({
                'message': 'Error en los tipos de datos',
                'error': str(e)
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'message': 'Error al crear el producto',
                'error': str(e)
            }, status=500)
    else:
        return JsonResponse({'message': 'Método no permitido'}, status=405)


# ============================================================================
# READ - Funciones para leer/consultar registros
# ============================================================================

# --- Funciones de lectura de Categorías ---

def listing(request):
    """Vista que lista las categorías disponibles en formato JSON."""
    # Obtener todas las categorías ordenadas por nombre
    categories = Category.objects.all().order_by('category_name')
    
    # Convertir a formato JSON
    categories_data = []
    for category in categories:
        categories_data.append({
            'category_id': category.category_id,
            'category_name': category.category_name,
            'category_description': category.category_description or '',
        })
    
    return JsonResponse(categories_data, safe=False, json_dumps_params={'ensure_ascii': False, 'indent': 2})

def category_list_by_license(request, license_name):
    """Vista que lista las categorías disponibles filtradas por licencia en formato JSON."""
    # Category no tiene relación directa con Licence, la relación es a través de Product
    categories = Category.objects.filter(
        product__licence__licence_name__icontains=license_name
    ).distinct().order_by('category_name')
    
    categories_data = []
    for category in categories:
        categories_data.append({
            'category_id': category.category_id,
            'category_name': category.category_name,
            'category_description': category.category_description or '',
        })
    return JsonResponse(categories_data, safe=False, json_dumps_params={'ensure_ascii': False, 'indent': 2})

def category(request, category_name):
    """Vista que lista los productos disponibles por categoría."""
    return HttpResponse(f"Listing products in category: {category_name}")

# --- Funciones de lectura de Licencias ---

def license_view(request):
    """Vista que lista todas las licencias disponibles en formato JSON."""
    licenses = Licence.objects.all().order_by('licence_id')
    licenses_data = []
    for licence_item in licenses:
        licenses_data.append({
            'licence_id': licence_item.licence_id,
            'licence_name': licence_item.licence_name,
            'licence_description': licence_item.licence_description or '',
            'licence_image': licence_item.licence_image or '',
        })
    return JsonResponse(licenses_data, safe=False, json_dumps_params={'ensure_ascii': False, 'indent': 2})

def license(request, license_name):
    """Vista que lista los productos disponibles por licencia."""
    # Filtrar por nombre de licencia si se proporciona
    if license_name:
        licenses = Licence.objects.filter(licence_name__icontains=license_name).order_by('licence_name')
    else:
        licenses = Licence.objects.all().order_by('licence_name')
    
    licenses_data = []
    for licence_item in licenses:
        licenses_data.append({
            'licence_id': licence_item.licence_id,
            'licence_name': licence_item.licence_name,
            'licence_description': licence_item.licence_description or '',
            'licence_image': licence_item.licence_image or '',
        })
    return JsonResponse(licenses_data, safe=False, json_dumps_params={'ensure_ascii': False, 'indent': 2})

# --- Funciones de lectura de Productos ---

def product_list(request):
    """Vista que lista todos los productos disponibles."""
    products = Product.objects.all().order_by('product_name')
    
    # Convertir a formato JSON
    products_data = []
    for product in products:
        products_data.append({
            'product_id': product.product_id,
            'product_name': product.product_name,
            'product_description': product.product_description,
            'price': float(product.price),
            'stock': product.stock,
            'discount': product.discount or 0,
            'sku': product.sku,
        })
    
    return JsonResponse(products_data, safe=False, json_dumps_params={'ensure_ascii': False, 'indent': 2})

def product_list_by_category(request, category_name):
    """Vista que lista todos los productos disponibles por categoría en formato JSON."""
    products = Product.objects.filter(category__category_name__icontains=category_name).order_by('product_name')
    products_data = []
    for product_item in products:
        products_data.append({
            'product_id': product_item.product_id,
            'product_name': product_item.product_name,
            'product_description': product_item.product_description,
            'price': float(product_item.price),
            'stock': product_item.stock,
            'discount': product_item.discount or 0,
            'sku': product_item.sku,
        })
    return JsonResponse(products_data, safe=False, json_dumps_params={'ensure_ascii': False, 'indent': 2})

def product_list_by_license(request, license_name):
    """Vista que lista todos los productos disponibles por licencia en formato JSON."""
    products = Product.objects.filter(licence__licence_name__icontains=license_name).order_by('product_name')
    products_data = []
    for product_item in products:
        products_data.append({
            'product_id': product_item.product_id,
            'product_name': product_item.product_name,
            'product_description': product_item.product_description,
            'price': float(product_item.price),
            'stock': product_item.stock,
            'discount': product_item.discount or 0,
            'sku': product_item.sku,
        })
    return JsonResponse(products_data, safe=False, json_dumps_params={'ensure_ascii': False, 'indent': 2})

def product(request, product_name):
    """Vista que lista el producto seleccionado."""
    return HttpResponse(f"Listing product: {product_name}")

# --- Funciones de búsqueda específica de Productos ---

def find_product_by_id(request, product_id):
    """Busca un producto por su ID en la base de datos."""
    if request.method == 'GET':
        try:
            product = Product.objects.get(product_id=product_id)
            product_data = {
                'product_id': product.product_id,
                'product_name': product.product_name,
                'product_description': product.product_description,
                'price': float(product.price),
                'stock': product.stock,
                'discount': product.discount or 0,
                'sku': product.sku,
                'image_front': product.image_front,
                'image_back': product.image_back,
                'licence': {
                    'licence_id': product.licence.licence_id,
                    'licence_name': product.licence.licence_name,
                },
                'category': {
                    'category_id': product.category.category_id,
                    'category_name': product.category.category_name,
                }
            }
            return JsonResponse(product_data, safe=False, json_dumps_params={'ensure_ascii': False, 'indent': 2})
        except Product.DoesNotExist:
            return JsonResponse({'message': 'Producto no encontrado'}, status=404)
        except Exception as e:
            return JsonResponse({'message': 'Error al buscar el producto', 'error': str(e)}, status=500)
    else:
        return JsonResponse({'message': 'Método no permitido'}, status=405)

def find_product_by_name(request, product_name):
    """Busca un producto por su nombre en la base de datos."""
    if request.method == 'GET':
        try:
            product = Product.objects.get(product_name=product_name)
            product_data = {
                'product_id': product.product_id,
                'product_name': product.product_name,
                'product_description': product.product_description,
                'price': float(product.price),
                'stock': product.stock,
                'discount': product.discount or 0,
                'sku': product.sku,
                'image_front': product.image_front,
                'image_back': product.image_back,
                'licence': {
                    'licence_id': product.licence.licence_id,
                    'licence_name': product.licence.licence_name,
                },
                'category': {
                    'category_id': product.category.category_id,
                    'category_name': product.category.category_name,
                }
            }
            return JsonResponse(product_data, safe=False, json_dumps_params={'ensure_ascii': False, 'indent': 2})
        except Product.DoesNotExist:
            return JsonResponse({'message': 'Producto no encontrado'}, status=404)
        except Product.MultipleObjectsReturned:
            return JsonResponse({'message': 'Múltiples productos encontrados con ese nombre'}, status=400)
        except Exception as e:
            return JsonResponse({'message': 'Error al buscar el producto', 'error': str(e)}, status=500)
    else:
        return JsonResponse({'message': 'Método no permitido'}, status=405)

def find_product_by_sku(request, sku):
    """Busca un producto por su SKU en la base de datos."""
    if request.method == 'GET':
        try:
            product = Product.objects.get(sku=sku)
            product_data = {
                'product_id': product.product_id,
                'product_name': product.product_name,
                'product_description': product.product_description,
                'price': float(product.price),
                'stock': product.stock,
                'discount': product.discount or 0,
                'sku': product.sku,
                'image_front': product.image_front,
                'image_back': product.image_back,
                'licence': {
                    'licence_id': product.licence.licence_id,
                    'licence_name': product.licence.licence_name,
                },
                'category': {
                    'category_id': product.category.category_id,
                    'category_name': product.category.category_name,
                }
            }
            return JsonResponse(product_data, safe=False, json_dumps_params={'ensure_ascii': False, 'indent': 2})
        except Product.DoesNotExist:
            return JsonResponse({'message': 'Producto no encontrado'}, status=404)
        except Exception as e:
            return JsonResponse({'message': 'Error al buscar el producto', 'error': str(e)}, status=500)
    else:
        return JsonResponse({'message': 'Método no permitido'}, status=405)


# ============================================================================
# UPDATE - Funciones para actualizar registros
# ============================================================================

def update_product(request, product_id):
    """Actualiza un producto existente en la base de datos."""
    if request.method == 'PUT' or request.method == 'POST':
        try:
            # Obtener el producto
            product = Product.objects.get(product_id=product_id)
            
            # Obtener datos del request (soporta tanto POST como datos JSON)
            if hasattr(request, 'data'):
                data = request.data
            else:
                data = request.POST
            
            # Actualizar campos si se proporcionan
            if 'product_name' in data:
                product.product_name = data.get('product_name')
            if 'product_description' in data:
                product.product_description = data.get('product_description')
            if 'price' in data:
                product.price = float(data.get('price'))
            if 'stock' in data:
                product.stock = int(data.get('stock'))
            if 'discount' in data:
                discount_value = data.get('discount')
                product.discount = int(discount_value) if discount_value else None
            if 'sku' in data:
                new_sku = data.get('sku')
                # Verificar que el SKU no esté en uso por otro producto
                if new_sku != product.sku and Product.objects.filter(sku=new_sku).exists():
                    return JsonResponse({
                        'message': 'El SKU ya está en uso por otro producto',
                        'sku': new_sku
                    }, status=400)
                product.sku = new_sku
            if 'image_front' in data:
                product.image_front = data.get('image_front', '')
            if 'image_back' in data:
                product.image_back = data.get('image_back', '')
            if 'dues' in data:
                dues_value = data.get('dues')
                product.dues = int(dues_value) if dues_value else None
            if 'created_by' in data:
                product.created_by = int(data.get('created_by'))
            
            # Actualizar licencia si se proporciona
            if 'licence' in data or 'licence_name' in data:
                licence_name = data.get('licence') or data.get('licence_name')
                licence_obj, _ = Licence.objects.get_or_create(
                    licence_name=licence_name,
                    defaults={
                        'licence_description': data.get('licence_description', f'Licencia {licence_name}'),
                        'licence_image': data.get('licence_image', '')
                    }
                )
                product.licence = licence_obj
            
            # Actualizar categoría si se proporciona
            if 'category' in data or 'category_name' in data:
                category_name = data.get('category') or data.get('category_name')
                category_obj, _ = Category.objects.get_or_create(
                    category_name=category_name,
                    defaults={
                        'category_description': data.get('category_description', f'Categoría {category_name}')
                    }
                )
                product.category = category_obj
            
            product.save()
            
            return JsonResponse({
                'message': 'Producto actualizado correctamente',
                'product_id': product.product_id,
                'product_name': product.product_name
            }, status=200)
            
        except Product.DoesNotExist:
            return JsonResponse({'message': 'Producto no encontrado'}, status=404)
        except ValueError as e:
            return JsonResponse({
                'message': 'Error en los tipos de datos',
                'error': str(e)
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'message': 'Error al actualizar el producto',
                'error': str(e)
            }, status=500)
    else:
        return JsonResponse({'message': 'Método no permitido'}, status=405)

def update_category(request, category_id):
    """Actualiza una categoría existente en la base de datos."""
    if request.method == 'PUT' or request.method == 'POST':
        try:
            category = Category.objects.get(category_id=category_id)
            
            # Obtener datos del request
            if hasattr(request, 'data'):
                data = request.data
            else:
                data = request.POST
            
            # Actualizar campos si se proporcionan
            if 'category_name' in data:
                category.category_name = data.get('category_name')
            if 'category_description' in data:
                category.category_description = data.get('category_description', '')
            
            category.save()
            
            return JsonResponse({
                'message': 'Categoría actualizada correctamente',
                'category_id': category.category_id,
                'category_name': category.category_name
            }, status=200)
            
        except Category.DoesNotExist:
            return JsonResponse({'message': 'Categoría no encontrada'}, status=404)
        except Exception as e:
            return JsonResponse({
                'message': 'Error al actualizar la categoría',
                'error': str(e)
            }, status=500)
    else:
        return JsonResponse({'message': 'Método no permitido'}, status=405)

def update_licence(request, licence_id):
    """Actualiza una licencia existente en la base de datos."""
    if request.method == 'PUT' or request.method == 'POST':
        try:
            licence = Licence.objects.get(licence_id=licence_id)
            
            # Obtener datos del request
            if hasattr(request, 'data'):
                data = request.data
            else:
                data = request.POST
            
            # Actualizar campos si se proporcionan
            if 'licence_name' in data:
                licence.licence_name = data.get('licence_name')
            if 'licence_description' in data:
                licence.licence_description = data.get('licence_description', '')
            if 'licence_image' in data:
                licence.licence_image = data.get('licence_image', '')
            
            licence.save()
            
            return JsonResponse({
                'message': 'Licencia actualizada correctamente',
                'licence_id': licence.licence_id,
                'licence_name': licence.licence_name
            }, status=200)
            
        except Licence.DoesNotExist:
            return JsonResponse({'message': 'Licencia no encontrada'}, status=404)
        except Exception as e:
            return JsonResponse({
                'message': 'Error al actualizar la licencia',
                'error': str(e)
            }, status=500)
    else:
        return JsonResponse({'message': 'Método no permitido'}, status=405)


# ============================================================================
# DELETE - Funciones para eliminar registros
# ============================================================================

def delete_product(request, product_id):
    """Elimina un producto de la base de datos."""
    if request.method == 'DELETE' or request.method == 'POST':
        try:
            product = Product.objects.get(product_id=product_id)
            product_name = product.product_name
            product_id_value = product.product_id
            
            product.delete()
            
            return JsonResponse({
                'message': 'Producto eliminado correctamente',
                'product_id': product_id_value,
                'product_name': product_name
            }, status=200)
            
        except Product.DoesNotExist:
            return JsonResponse({'message': 'Producto no encontrado'}, status=404)
        except Exception as e:
            return JsonResponse({
                'message': 'Error al eliminar el producto',
                'error': str(e)
            }, status=500)
    else:
        return JsonResponse({'message': 'Método no permitido'}, status=405)

def delete_category(request, category_id):
    """Elimina una categoría de la base de datos.
    
    Nota: Si la categoría tiene productos asociados, la eliminación puede fallar
    dependiendo de la configuración de la base de datos.
    """
    if request.method == 'DELETE' or request.method == 'POST':
        try:
            category = Category.objects.get(category_id=category_id)
            category_name = category.category_name
            category_id_value = category.category_id
            
            # Verificar si hay productos asociados
            products_count = Product.objects.filter(category=category).count()
            if products_count > 0:
                return JsonResponse({
                    'message': f'No se puede eliminar la categoría porque tiene {products_count} producto(s) asociado(s)',
                    'category_id': category_id_value,
                    'products_count': products_count
                }, status=400)
            
            category.delete()
            
            return JsonResponse({
                'message': 'Categoría eliminada correctamente',
                'category_id': category_id_value,
                'category_name': category_name
            }, status=200)
            
        except Category.DoesNotExist:
            return JsonResponse({'message': 'Categoría no encontrada'}, status=404)
        except Exception as e:
            return JsonResponse({
                'message': 'Error al eliminar la categoría',
                'error': str(e)
            }, status=500)
    else:
        return JsonResponse({'message': 'Método no permitido'}, status=405)

def delete_licence(request, licence_id):
    """Elimina una licencia de la base de datos.
    
    Nota: Si la licencia tiene productos asociados, la eliminación puede fallar
    dependiendo de la configuración de la base de datos.
    """
    if request.method == 'DELETE' or request.method == 'POST':
        try:
            licence = Licence.objects.get(licence_id=licence_id)
            licence_name = licence.licence_name
            licence_id_value = licence.licence_id
            
            # Verificar si hay productos asociados
            products_count = Product.objects.filter(licence=licence).count()
            if products_count > 0:
                return JsonResponse({
                    'message': f'No se puede eliminar la licencia porque tiene {products_count} producto(s) asociado(s)',
                    'licence_id': licence_id_value,
                    'products_count': products_count
                }, status=400)
            
            licence.delete()
            
            return JsonResponse({
                'message': 'Licencia eliminada correctamente',
                'licence_id': licence_id_value,
                'licence_name': licence_name
            }, status=200)
            
        except Licence.DoesNotExist:
            return JsonResponse({'message': 'Licencia no encontrada'}, status=404)
        except Exception as e:
            return JsonResponse({
                'message': 'Error al eliminar la licencia',
                'error': str(e)
            }, status=500)
    else:
        return JsonResponse({'message': 'Método no permitido'}, status=405)
