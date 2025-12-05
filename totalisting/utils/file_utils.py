"""
Utilidades para manejo de archivos e imágenes.
"""

import os
import json
from pathlib import Path
from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile, TemporaryUploadedFile


def sanitize_filename(filename: str) -> str:
    """
    Sanitiza el nombre de archivo para evitar caracteres problemáticos.
    
    Args:
        filename: Nombre original del archivo
        
    Returns:
        Nombre sanitizado
    """
    # Reemplazar espacios y caracteres especiales
    filename = filename.replace(' ', '-').lower()
    # Remover caracteres no permitidos
    allowed_chars = '-_.()abcdefghijklmnopqrstuvwxyz0123456789'
    filename = ''.join(c if c in allowed_chars else '' for c in filename)
    return filename


def create_directory_if_not_exists(directory_path: str) -> bool:
    """
    Crea un directorio si no existe.
    
    Args:
        directory_path: Ruta del directorio a crear
        
    Returns:
        True si se creó o ya existía, False si hubo error
    """
    try:
        Path(directory_path).mkdir(parents=True, exist_ok=True)
        return True
    except Exception as e:
        print(f"Error al crear directorio {directory_path}: {str(e)}")
        return False


def save_uploaded_file(file, destination_path: str) -> bool:
    """
    Guarda un archivo subido en la ruta especificada.
    
    Args:
        file: Archivo subido (InMemoryUploadedFile o TemporaryUploadedFile)
        destination_path: Ruta completa donde guardar el archivo
        
    Returns:
        True si se guardó correctamente, False en caso contrario
    """
    try:
        # Crear directorio si no existe
        directory = os.path.dirname(destination_path)
        create_directory_if_not_exists(directory)
        
        # Guardar el archivo
        with open(destination_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        
        return True
    except Exception as e:
        print(f"Error al guardar archivo {destination_path}: {str(e)}")
        return False


def get_frontend_media_path(relative_path: str) -> str:
    """
    Convierte una ruta relativa a la ruta completa en el frontend.
    
    Args:
        relative_path: Ruta relativa (ej: /star-wars/baby-yoda-1.webp)
        
    Returns:
        Ruta completa para el frontend
    """
    # Si ya empieza con /multimedia/, mantenerla
    if relative_path.startswith('/multimedia/'):
        return relative_path
    
    # Si empieza con /, agregar multimedia
    if relative_path.startswith('/'):
        return f'/multimedia{relative_path}'
    
    # Si no empieza con /, agregar /multimedia/
    return f'/multimedia/{relative_path}'


def save_product_images(
    front_image,
    back_image,
    additional_images: list,
    licence_name: str,
    product_name: str,
    base_path: str = None
) -> dict:
    """
    Guarda las imágenes de un producto en la estructura de carpetas correcta.
    
    Estructura: frontend-shop/public/multimedia/{licence}/{product_name}/
    
    Args:
        front_image: Primera imagen (frontal, -1.webp)
        back_image: Segunda imagen (reverso, -box.webp)
        additional_images: Lista de imágenes adicionales
        licence_name: Nombre de la licencia (para la carpeta)
        product_name: Nombre del producto (para la carpeta)
        base_path: Ruta base del proyecto frontend (opcional)
        
    Returns:
        Diccionario con las rutas guardadas:
        {
            'image_front': '/licence/product-name-1.webp',
            'image_back': '/licence/product-name-box.webp',
            'additional_images': ['/licence/product-name-2.webp', ...]
        }
    """
    if base_path is None:
        # Ruta por defecto: ir dos niveles arriba desde backend-shop
        base_path = Path(__file__).resolve().parent.parent.parent.parent / 'frontend-shop' / 'public' / 'multimedia'
    
    # Sanitizar nombres
    sanitized_licence = sanitize_filename(licence_name)
    sanitized_product = sanitize_filename(product_name)
    
    # Crear ruta de carpeta del producto
    product_dir = Path(base_path) / sanitized_licence / sanitized_product
    
    # Crear directorio si no existe
    create_directory_if_not_exists(str(product_dir))
    
    results = {
        'image_front': None,
        'image_back': None,
        'additional_images': []
    }
    
    # Guardar imagen frontal
    if front_image:
        front_filename = f"{sanitized_product}-1.webp"
        front_path = product_dir / front_filename
        if save_uploaded_file(front_image, str(front_path)):
            # Ruta relativa para la BD: /licence/product-name-1.webp
            results['image_front'] = f"/{sanitized_licence}/{sanitized_product}/{front_filename}"
    
    # Guardar imagen reverso
    if back_image:
        back_filename = f"{sanitized_product}-box.webp"
        back_path = product_dir / back_filename
        if save_uploaded_file(back_image, str(back_path)):
            results['image_back'] = f"/{sanitized_licence}/{sanitized_product}/{back_filename}"
    
    # Guardar imágenes adicionales
    for idx, additional_img in enumerate(additional_images, start=2):
        if additional_img:
            additional_filename = f"{sanitized_product}-{idx}.webp"
            additional_path = product_dir / additional_filename
            if save_uploaded_file(additional_img, str(additional_path)):
                results['additional_images'].append(
                    f"/{sanitized_licence}/{sanitized_product}/{additional_filename}"
                )
    
    return results


def save_category_image(image, category_name: str, base_path: str = None) -> str:
    """
    Guarda la imagen de una categoría.
    
    Args:
        image: Archivo de imagen
        category_name: Nombre de la categoría
        base_path: Ruta base del proyecto frontend (opcional)
        
    Returns:
        Ruta relativa de la imagen guardada o None si hubo error
    """
    if base_path is None:
        base_path = Path(__file__).resolve().parent.parent.parent.parent / 'frontend-shop' / 'public' / 'multimedia'
    
    sanitized_category = sanitize_filename(category_name)
    category_dir = Path(base_path) / 'categories'
    create_directory_if_not_exists(str(category_dir))
    
    # Obtener extensión del archivo original
    original_filename = image.name if hasattr(image, 'name') else 'image.webp'
    extension = os.path.splitext(original_filename)[1] or '.webp'
    
    filename = f"{sanitized_category}{extension}"
    file_path = category_dir / filename
    
    if save_uploaded_file(image, str(file_path)):
        return f"/categories/{filename}"
    
    return None


def save_licence_image(image, licence_name: str, base_path: str = None) -> str:
    """
    Guarda la imagen de una licencia.
    
    Args:
        image: Archivo de imagen
        licence_name: Nombre de la licencia
        base_path: Ruta base del proyecto frontend (opcional)
        
    Returns:
        Ruta relativa de la imagen guardada o None si hubo error
    """
    if base_path is None:
        base_path = Path(__file__).resolve().parent.parent.parent.parent / 'frontend-shop' / 'public' / 'multimedia'
    
    sanitized_licence = sanitize_filename(licence_name)
    licence_dir = Path(base_path) / 'licences'
    create_directory_if_not_exists(str(licence_dir))
    
    # Obtener extensión del archivo original
    original_filename = image.name if hasattr(image, 'name') else 'image.webp'
    extension = os.path.splitext(original_filename)[1] or '.webp'
    
    filename = f"{sanitized_licence}{extension}"
    file_path = licence_dir / filename
    
    if save_uploaded_file(image, str(file_path)):
        return f"/licences/{filename}"
    
    return None

