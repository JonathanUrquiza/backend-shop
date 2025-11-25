"""
Tests unitarios para las factories.

Prueba la creación de objetos complejos mediante factories.
"""

from django.test import TestCase, TransactionTestCase
from totalisting.models import Product, Category, Licence
from totalisting.factories import ProductFactory
from .test_helpers import create_test_tables


class ProductFactoryTest(TransactionTestCase):
    """Tests para ProductFactory."""
    
    def setUp(self):
        """Configuración inicial para cada test."""
        # Crear las tablas necesarias para los tests
        create_test_tables()
        
        # Crear licencia de prueba
        self.licence = Licence.objects.create(
            licence_name='Test Licence Factory',
            licence_description='Test Description',
            licence_image='test.jpg'
        )
        
        # Crear categoría de prueba
        self.category = Category.objects.create(
            category_name='Test Category Factory',
            category_description='Test Description'
        )
    
    def test_create_product_with_existing_relations(self):
        """Test que verifica crear producto con licencia y categoría existentes."""
        data = {
            'product_name': 'Factory Product',
            'product_description': 'Test Description',
            'price': '99.99',
            'stock': '10',
            'sku': 'FACTORY-001',
            'licence': 'Test Licence Factory',
            'category': 'Test Category Factory'
        }
        
        product, error, metadata = ProductFactory.create_product(data)
        
        self.assertIsNotNone(product)
        self.assertIsNone(error)
        self.assertEqual(product.product_name, 'Factory Product')
        self.assertEqual(product.licence.licence_name, 'Test Licence Factory')
        self.assertEqual(product.category.category_name, 'Test Category Factory')
        self.assertFalse(metadata['licence']['created'])  # No se creó, ya existía
        self.assertFalse(metadata['category']['created'])  # No se creó, ya existía
        
        # Limpiar
        product.delete()
    
    def test_create_product_with_new_relations(self):
        """Test que verifica crear producto creando nuevas licencia y categoría."""
        data = {
            'product_name': 'Factory Product New Relations',
            'product_description': 'Test Description',
            'price': '99.99',
            'stock': '10',
            'sku': 'FACTORY-NEW-001',
            'licence': 'New Licence Factory',
            'category': 'New Category Factory',
            'licence_description': 'New Licence Description',
            'category_description': 'New Category Description'
        }
        
        product, error, metadata = ProductFactory.create_product(data)
        
        self.assertIsNotNone(product)
        self.assertIsNone(error)
        self.assertEqual(product.product_name, 'Factory Product New Relations')
        self.assertTrue(metadata['licence']['created'])  # Se creó nueva licencia
        self.assertTrue(metadata['category']['created'])  # Se creó nueva categoría
        
        # Limpiar
        product.delete()
        product.licence.delete()
        product.category.delete()
    
    def test_create_product_duplicate_sku(self):
        """Test que verifica que no se puede crear producto con SKU duplicado."""
        # Crear producto primero
        product = Product.objects.create(
            product_name='Existing Factory Product',
            product_description='Test',
            price=99.99,
            stock=10,
            sku='FACTORY-DUPLICATE-001',
            licence=self.licence,
            category=self.category,
            created_by=1,
            image_front='',
            image_back=''
        )
        
        # Intentar crear otro con el mismo SKU
        data = {
            'product_name': 'Duplicate Factory Product',
            'product_description': 'Test',
            'price': '50.00',
            'stock': '5',
            'sku': 'FACTORY-DUPLICATE-001',
            'licence': 'Test Licence Factory',
            'category': 'Test Category Factory'
        }
        
        new_product, error, metadata = ProductFactory.create_product(data)
        
        self.assertIsNone(new_product)
        self.assertIsNotNone(error)
        self.assertIn('SKU', error)
        
        # Limpiar
        product.delete()
    
    def test_create_product_invalid_data(self):
        """Test que verifica que no se puede crear producto con datos inválidos."""
        data = {
            'product_name': 'Invalid Product',
            # Faltan campos obligatorios
        }
        
        product, error, metadata = ProductFactory.create_product(data)
        
        self.assertIsNone(product)
        self.assertIsNotNone(error)
        self.assertIn('Faltan campos obligatorios', error)
    
    def test_create_product_invalid_price_type(self):
        """Test que verifica validación de tipo de precio."""
        data = {
            'product_name': 'Invalid Price Product',
            'product_description': 'Test',
            'price': 'invalid_price',  # Precio inválido
            'stock': '10',
            'sku': 'FACTORY-INVALID-001',
            'licence': 'Test Licence Factory',
            'category': 'Test Category Factory'
        }
        
        product, error, metadata = ProductFactory.create_product(data)
        
        self.assertIsNone(product)
        self.assertIsNotNone(error)
        self.assertIn('Error en los tipos de datos', error)

