"""
Utilidades para manejo de archivos e imágenes.

Este módulo contiene funciones auxiliares para:
- Sanitizar nombres de archivos
- Crear directorios
- Guardar archivos subidos
- Manejar rutas de imágenes para productos, categorías y licencias

Todas las funciones trabajan con la estructura de carpetas del frontend:
- frontend-shop/public/multimedia/{tipo}/{nombre}/
"""

# Importar módulo os para operaciones del sistema operativo
import os
# Importar módulo json para serializar/deserializar datos JSON
import json
# Importar Path de pathlib para manejo de rutas multiplataforma
from pathlib import Path
# Importar settings de Django para acceder a configuración
from django.conf import settings
# Importar tipos de archivos subidos de Django
from django.core.files.uploadedfile import InMemoryUploadedFile, TemporaryUploadedFile


def sanitize_filename(filename: str) -> str:
    """
    Sanitiza el nombre de archivo para evitar caracteres problemáticos.
    
    Esta función limpia el nombre de archivo para que sea seguro usarlo en rutas
    del sistema de archivos. Convierte a minúsculas, reemplaza espacios por guiones
    y elimina caracteres especiales que podrían causar problemas.
    
    Args:
        filename: Nombre original del archivo (ej: "Baby Yoda Blueball")
        
    Returns:
        str: Nombre sanitizado (ej: "baby-yoda-blueball")
        
    Ejemplo:
        >>> sanitize_filename("Star Wars - Baby Yoda!")
        'star-wars---baby-yoda'
    """
    # Reemplazar espacios por guiones y convertir a minúsculas
    # Esto hace que los nombres sean más consistentes y seguros para URLs
    filename = filename.replace(' ', '-').lower()
    
    # Definir caracteres permitidos en nombres de archivo
    # Incluye: guiones, guiones bajos, puntos, paréntesis, letras y números
    allowed_chars = '-_.()abcdefghijklmnopqrstuvwxyz0123456789'
    
    # Filtrar solo los caracteres permitidos, eliminando cualquier otro carácter
    # Esto previene problemas con caracteres especiales en diferentes sistemas operativos
    filename = ''.join(c if c in allowed_chars else '' for c in filename)
    
    return filename


def create_directory_if_not_exists(directory_path: str) -> bool:
    """
    Crea un directorio si no existe.
    
    Esta función crea un directorio y todos sus padres necesarios si no existen.
    Si el directorio ya existe, no hace nada (no lanza error).
    
    Args:
        directory_path: Ruta completa del directorio a crear
                       (ej: "/path/to/frontend-shop/public/multimedia/star-wars")
        
    Returns:
        bool: True si se creó exitosamente o ya existía, False si hubo error
        
    Ejemplo:
        >>> create_directory_if_not_exists("/path/to/new/directory")
        True
    """
    try:
        # Crear el directorio usando Path de pathlib
        # parents=True: Crea todos los directorios padres necesarios
        # exist_ok=True: No lanza error si el directorio ya existe
        Path(directory_path).mkdir(parents=True, exist_ok=True)
        return True  # Retornar True si se creó exitosamente
    except Exception as e:
        # Si hay algún error (permisos, disco lleno, etc.), imprimir y retornar False
        print(f"Error al crear directorio {directory_path}: {str(e)}")
        return False


def save_uploaded_file(file, destination_path: str) -> bool:
    """
    Guarda un archivo subido en la ruta especificada.
    
    Esta función guarda un archivo subido desde un formulario Django en el sistema
    de archivos. Crea el directorio de destino si no existe y guarda el archivo
    en chunks para manejar archivos grandes eficientemente.
    
    Args:
        file: Archivo subido de Django (InMemoryUploadedFile o TemporaryUploadedFile)
              Este es el objeto que Django crea cuando se sube un archivo
        destination_path: Ruta completa donde guardar el archivo
                         (ej: "/path/to/file/image.webp")
        
    Returns:
        bool: True si se guardó correctamente, False si hubo error
        
    Ejemplo:
        >>> save_uploaded_file(uploaded_file, "/path/to/save/image.webp")
        True
    """
    try:
        # Extraer el directorio de la ruta de destino
        # os.path.dirname obtiene la parte del directorio sin el nombre del archivo
        directory = os.path.dirname(destination_path)
        
        # Crear el directorio si no existe (incluyendo todos los padres necesarios)
        create_directory_if_not_exists(directory)
        
        # Guardar el archivo en modo binario de escritura ('wb+')
        # 'wb+': write binary + permite lectura/escritura
        with open(destination_path, 'wb+') as destination:
            # Leer el archivo en chunks (pedazos) para manejar archivos grandes
            # file.chunks() es un generador que devuelve el archivo en partes
            # Esto es más eficiente en memoria que leer todo el archivo de una vez
            for chunk in file.chunks():
                # Escribir cada chunk al archivo de destino
                destination.write(chunk)
        
        return True  # Retornar True si se guardó exitosamente
    except Exception as e:
        # Si hay algún error (permisos, disco lleno, etc.), imprimir y retornar False
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
    
    Esta función organiza las imágenes de un producto en una estructura jerárquica:
    frontend-shop/public/multimedia/{licence}/{product_name}/
    
    Convención de nombres:
    - Imagen frontal: {product-name}-1.webp (primera imagen, se muestra en lista)
    - Imagen reverso: {product-name}-box.webp (segunda imagen, reverso del empaque)
    - Imágenes adicionales: {product-name}-2.webp, {product-name}-3.webp, etc.
    
    Args:
        front_image: Primera imagen (frontal) - archivo subido o None
        back_image: Segunda imagen (reverso del empaque) - archivo subido o None
        additional_images: Lista de imágenes adicionales para vista de detalle
        licence_name: Nombre de la licencia (ej: "Star Wars") - usado para crear carpeta
        product_name: Nombre del producto (ej: "Baby Yoda") - usado para crear carpeta
        base_path: Ruta base del proyecto frontend (opcional, se calcula si es None)
        
    Returns:
        dict: Diccionario con las rutas relativas guardadas:
        {
            'image_front': '/star-wars/baby-yoda-1.webp' o None,
            'image_back': '/star-wars/baby-yoda-box.webp' o None,
            'additional_images': ['/star-wars/baby-yoda-2.webp', ...] o []
        }
        
    Ejemplo:
        >>> save_product_images(front_img, back_img, [img1, img2], "Star Wars", "Baby Yoda")
        {
            'image_front': '/star-wars/baby-yoda-1.webp',
            'image_back': '/star-wars/baby-yoda-box.webp',
            'additional_images': ['/star-wars/baby-yoda-2.webp', '/star-wars/baby-yoda-3.webp']
        }
    """
    # Si no se proporciona base_path, calcularlo automáticamente
    if base_path is None:
        # Obtener la ruta del archivo actual y navegar hacia el frontend
        # __file__ es la ruta de este archivo (file_utils.py)
        # .resolve() convierte a ruta absoluta
        # .parent.parent.parent.parent navega: utils -> totalisting -> backend-shop -> raíz
        # Luego va a frontend-shop/public/multimedia
        base_path = Path(__file__).resolve().parent.parent.parent.parent / 'frontend-shop' / 'public' / 'multimedia'
    
    # Sanitizar nombres para que sean seguros para usar en rutas del sistema de archivos
    # Esto convierte "Star Wars" -> "star-wars" y "Baby Yoda!" -> "baby-yoda"
    sanitized_licence = sanitize_filename(licence_name)
    sanitized_product = sanitize_filename(product_name)
    
    # Crear ruta completa de la carpeta del producto
    # Ejemplo: /path/to/frontend-shop/public/multimedia/star-wars/baby-yoda
    product_dir = Path(base_path) / sanitized_licence / sanitized_product
    
    # Crear el directorio del producto si no existe (incluyendo carpetas padre)
    create_directory_if_not_exists(str(product_dir))
    
    # Inicializar diccionario de resultados con valores por defecto
    results = {
        'image_front': None,  # Ruta de imagen frontal (None si no se proporcionó)
        'image_back': None,  # Ruta de imagen reverso (None si no se proporcionó)
        'additional_images': []  # Lista de rutas de imágenes adicionales (vacía por defecto)
    }
    
    # Guardar imagen frontal si se proporcionó
    if front_image:  # Si hay una imagen frontal
        # Generar nombre del archivo: {product-name}-1.webp
        # Ejemplo: "baby-yoda-1.webp"
        front_filename = f"{sanitized_product}-1.webp"
        
        # Crear ruta completa del archivo
        front_path = product_dir / front_filename
        
        # Guardar el archivo en el sistema de archivos
        if save_uploaded_file(front_image, str(front_path)):
            # Si se guardó exitosamente, agregar ruta relativa al resultado
            # Ruta relativa para la BD: /licence/product-name-1.webp
            # Esta ruta se almacena en la base de datos
            results['image_front'] = f"/{sanitized_licence}/{sanitized_product}/{front_filename}"
    
    # Guardar imagen reverso si se proporcionó
    if back_image:  # Si hay una imagen reverso
        # Generar nombre del archivo: {product-name}-box.webp
        # Ejemplo: "baby-yoda-box.webp"
        back_filename = f"{sanitized_product}-box.webp"
        
        # Crear ruta completa del archivo
        back_path = product_dir / back_filename
        
        # Guardar el archivo en el sistema de archivos
        if save_uploaded_file(back_image, str(back_path)):
            # Si se guardó exitosamente, agregar ruta relativa al resultado
            results['image_back'] = f"/{sanitized_licence}/{sanitized_product}/{back_filename}"
    
    # Guardar imágenes adicionales (para vista de detalle del producto)
    # enumerate(additional_images, start=2): empieza desde índice 2
    # Esto significa que las imágenes adicionales serán: -2.webp, -3.webp, -4.webp, etc.
    for idx, additional_img in enumerate(additional_images, start=2):
        if additional_img:  # Si hay una imagen adicional
            # Generar nombre del archivo: {product-name}-{idx}.webp
            # Ejemplo: "baby-yoda-2.webp", "baby-yoda-3.webp"
            additional_filename = f"{sanitized_product}-{idx}.webp"
            
            # Crear ruta completa del archivo
            additional_path = product_dir / additional_filename
            
            # Guardar el archivo en el sistema de archivos
            if save_uploaded_file(additional_img, str(additional_path)):
                # Si se guardó exitosamente, agregar ruta relativa a la lista
                results['additional_images'].append(
                    f"/{sanitized_licence}/{sanitized_product}/{additional_filename}"
                )
    
    # Retornar diccionario con todas las rutas guardadas
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

