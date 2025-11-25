"""
Tests principales para totalisting.

Este archivo importa todos los tests de los submódulos.
Los tests están organizados en:
- test_serializers.py: Tests para serializers
- test_repositories.py: Tests para repositorios
- test_services.py: Tests para servicios
- test_factories.py: Tests para factories
"""

# Importar todos los tests para que Django los descubra
from .tests.test_serializers import *
from .tests.test_repositories import *
from .tests.test_services import *
from .tests.test_factories import *
