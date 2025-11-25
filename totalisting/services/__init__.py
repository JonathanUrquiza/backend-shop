"""
Módulo de servicios para totalisting.

Este módulo contiene la lógica de negocio separada de las vistas.
"""

from .product_service import ProductService
from .category_service import CategoryService
from .licence_service import LicenceService

__all__ = ['ProductService', 'CategoryService', 'LicenceService']

