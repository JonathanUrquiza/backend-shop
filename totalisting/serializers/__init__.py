"""
Módulo de serializers para totalisting.

Este módulo contiene los serializers/DTOs para convertir modelos a JSON y viceversa.
"""

from .product_serializer import ProductSerializer
from .category_serializer import CategorySerializer
from .licence_serializer import LicenceSerializer

__all__ = ['ProductSerializer', 'CategorySerializer', 'LicenceSerializer']

