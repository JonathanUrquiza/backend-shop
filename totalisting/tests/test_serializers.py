"""
Tests unitarios para los serializers.

Prueba la funcionalidad de serialización de modelos a diccionarios JSON.
"""

from django.test import TestCase
from totalisting.models import Product, Category, Licence
from totalisting.serializers import ProductSerializer, CategorySerializer, LicenceSerializer


class ProductSerializerTest(TestCase):
    """Tests para ProductSerializer."""
    
    def setUp(self):
        """Configuración inicial para cada test."""
        # Crear licencia de prueba
        self.licence = Licence(
            licence_id=1,
            licence_name='Test Licence',
            licence_description='Test Description',
            licence_image='test.jpg'
        )
        
        # Crear categoría de prueba
        self.category = Category(
            category_id=1,
            category_name='Test Category',
            category_description='Test Category Description'
        )
        
        # Crear producto de prueba
        self.product = Product(
            product_id=1,
            product_name='Test Product',
            product_description='Test Description',
            price=99.99,
            stock=10,
            discount=5,
            sku='TEST-001',
            dues=3,
            created_by=1,
            image_front='front.jpg',
            image_back='back.jpg',
            licence=self.licence,
            category=self.category
        )
    
    def test_to_dict_with_relations(self):
        """Test que verifica la serialización con relaciones."""
        result = ProductSerializer.to_dict(self.product, include_relations=True)
        
        self.assertIsInstance(result, dict)
        self.assertEqual(result['product_id'], 1)
        self.assertEqual(result['product_name'], 'Test Product')
        self.assertEqual(result['price'], 99.99)
        self.assertEqual(result['stock'], 10)
        self.assertEqual(result['discount'], 5)
        self.assertEqual(result['sku'], 'TEST-001')
        self.assertIn('licence', result)
        self.assertIn('category', result)
        self.assertEqual(result['licence']['licence_name'], 'Test Licence')
        self.assertEqual(result['category']['category_name'], 'Test Category')
    
    def test_to_dict_without_relations(self):
        """Test que verifica la serialización sin relaciones."""
        result = ProductSerializer.to_dict(self.product, include_relations=False)
        
        self.assertIsInstance(result, dict)
        self.assertEqual(result['product_id'], 1)
        self.assertEqual(result['product_name'], 'Test Product')
        self.assertNotIn('licence', result)
        self.assertNotIn('category', result)
    
    def test_to_dict_list(self):
        """Test que verifica la serialización de una lista de productos."""
        products = [self.product]
        result = ProductSerializer.to_dict_list(products, include_relations=False)
        
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['product_name'], 'Test Product')
    
    def test_validate_create_data_success(self):
        """Test que verifica la validación exitosa de datos."""
        data = {
            'product_name': 'New Product',
            'product_description': 'Description',
            'price': '50.00',
            'stock': '5',
            'sku': 'NEW-001',
            'licence': 'New Licence',
            'category': 'New Category'
        }
        
        is_valid, error, validated = ProductSerializer.validate_create_data(data)
        
        self.assertTrue(is_valid)
        self.assertIsNone(error)
        self.assertEqual(validated['product_name'], 'New Product')
        self.assertEqual(validated['price'], 50.0)
        self.assertEqual(validated['stock'], 5)
    
    def test_validate_create_data_missing_fields(self):
        """Test que verifica la validación con campos faltantes."""
        data = {
            'product_name': 'New Product',
            # Faltan campos obligatorios
        }
        
        is_valid, error, validated = ProductSerializer.validate_create_data(data)
        
        self.assertFalse(is_valid)
        self.assertIsNotNone(error)
        self.assertIn('Faltan campos obligatorios', error)
    
    def test_validate_create_data_invalid_types(self):
        """Test que verifica la validación con tipos de datos inválidos."""
        data = {
            'product_name': 'New Product',
            'product_description': 'Description',
            'price': 'invalid',  # Precio inválido
            'stock': '5',
            'sku': 'NEW-001',
            'licence': 'New Licence',
            'category': 'New Category'
        }
        
        is_valid, error, validated = ProductSerializer.validate_create_data(data)
        
        self.assertFalse(is_valid)
        self.assertIsNotNone(error)
        self.assertIn('Error en los tipos de datos', error)


class CategorySerializerTest(TestCase):
    """Tests para CategorySerializer."""
    
    def setUp(self):
        """Configuración inicial para cada test."""
        self.category = Category(
            category_id=1,
            category_name='Test Category',
            category_description='Test Description'
        )
    
    def test_to_dict(self):
        """Test que verifica la serialización de categoría."""
        result = CategorySerializer.to_dict(self.category)
        
        self.assertIsInstance(result, dict)
        self.assertEqual(result['category_id'], 1)
        self.assertEqual(result['category_name'], 'Test Category')
        self.assertEqual(result['category_description'], 'Test Description')
    
    def test_to_dict_list(self):
        """Test que verifica la serialización de una lista de categorías."""
        categories = [self.category]
        result = CategorySerializer.to_dict_list(categories)
        
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['category_name'], 'Test Category')
    
    def test_to_dict_with_null_description(self):
        """Test que verifica la serialización con descripción nula."""
        category = Category(
            category_id=2,
            category_name='Category Without Description',
            category_description=None
        )
        
        result = CategorySerializer.to_dict(category)
        
        self.assertEqual(result['category_description'], '')


class LicenceSerializerTest(TestCase):
    """Tests para LicenceSerializer."""
    
    def setUp(self):
        """Configuración inicial para cada test."""
        self.licence = Licence(
            licence_id=1,
            licence_name='Test Licence',
            licence_description='Test Description',
            licence_image='test.jpg'
        )
    
    def test_to_dict(self):
        """Test que verifica la serialización de licencia."""
        result = LicenceSerializer.to_dict(self.licence)
        
        self.assertIsInstance(result, dict)
        self.assertEqual(result['licence_id'], 1)
        self.assertEqual(result['licence_name'], 'Test Licence')
        self.assertEqual(result['licence_description'], 'Test Description')
        self.assertEqual(result['licence_image'], 'test.jpg')
    
    def test_to_dict_list(self):
        """Test que verifica la serialización de una lista de licencias."""
        licences = [self.licence]
        result = LicenceSerializer.to_dict_list(licences)
        
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['licence_name'], 'Test Licence')
    
    def test_to_dict_with_null_fields(self):
        """Test que verifica la serialización con campos nulos."""
        licence = Licence(
            licence_id=2,
            licence_name='Licence Without Image',
            licence_description='Description',
            licence_image=None
        )
        
        result = LicenceSerializer.to_dict(licence)
        
        self.assertEqual(result['licence_image'], '')

