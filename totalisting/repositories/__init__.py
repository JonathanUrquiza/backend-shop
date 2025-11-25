"""
Módulo de repositorios para totalisting.

Este módulo contiene los repositorios que abstraen el acceso a datos.
"""

from .product_repository import ProductRepository
from .category_repository import CategoryRepository
from .licence_repository import LicenceRepository

__all__ = ['ProductRepository', 'CategoryRepository', 'LicenceRepository']

