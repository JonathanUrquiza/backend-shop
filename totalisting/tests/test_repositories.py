"""
Tests unitarios para los repositorios.

Prueba la funcionalidad de acceso a datos mediante repositorios.
"""

from django.test import TestCase, TransactionTestCase
from django.core.exceptions import ObjectDoesNotExist
from totalisting.models import Product, Category, Licence
from totalisting.repositories import (
    ProductRepository,
    CategoryRepository,
    LicenceRepository
)
from .test_helpers import create_test_tables


class ProductRepositoryTest(TransactionTestCase):
    """Tests para ProductRepository."""
    
    def setUp(self):
        """Configuración inicial para cada test."""
        # Crear las tablas necesarias para los tests
        create_test_tables()
        
        # Crear licencia de prueba
        self.licence = Licence.objects.create(
            licence_name='Test Licence',
            licence_description='Test Description',
            licence_image='test.jpg'
        )
        
        # Crear categoría de prueba
        self.category = Category.objects.create(
            category_name='Test Category',
            category_description='Test Description'
        )
    
    def test_get_all_products(self):
        """Test que verifica obtener todos los productos."""
        products = ProductRepository.get_all()
        
        self.assertIsInstance(products, list)
        # Verificar que todos son instancias de Product
        for product in products:
            self.assertIsInstance(product, Product)
    
    def test_get_by_id_existing(self):
        """Test que verifica obtener un producto por ID existente."""
        # Crear producto de prueba
        product = Product.objects.create(
            product_name='Test Product',
            product_description='Test',
            price=99.99,
            stock=10,
            sku='TEST-REPO-001',
            licence=self.licence,
            category=self.category,
            created_by=1,
            image_front='',
            image_back=''
        )
        
        result = ProductRepository.get_by_id(product.product_id)
        
        self.assertIsNotNone(result)
        self.assertEqual(result.product_id, product.product_id)
        self.assertEqual(result.product_name, 'Test Product')
        
        # Limpiar
        product.delete()
    
    def test_get_by_id_nonexistent(self):
        """Test que verifica obtener un producto por ID inexistente."""
        result = ProductRepository.get_by_id(99999)
        
        self.assertIsNone(result)
    
    def test_get_by_sku_existing(self):
        """Test que verifica obtener un producto por SKU existente."""
        # Crear producto de prueba
        product = Product.objects.create(
            product_name='Test Product SKU',
            product_description='Test',
            price=99.99,
            stock=10,
            sku='TEST-REPO-SKU-001',
            licence=self.licence,
            category=self.category,
            created_by=1,
            image_front='',
            image_back=''
        )
        
        result = ProductRepository.get_by_sku('TEST-REPO-SKU-001')
        
        self.assertIsNotNone(result)
        self.assertEqual(result.sku, 'TEST-REPO-SKU-001')
        
        # Limpiar
        product.delete()
    
    def test_sku_exists(self):
        """Test que verifica si un SKU existe."""
        # Crear producto de prueba
        product = Product.objects.create(
            product_name='Test Product SKU Check',
            product_description='Test',
            price=99.99,
            stock=10,
            sku='TEST-REPO-SKU-CHECK',
            licence=self.licence,
            category=self.category,
            created_by=1,
            image_front='',
            image_back=''
        )
        
        # Verificar que existe
        self.assertTrue(ProductRepository.sku_exists('TEST-REPO-SKU-CHECK'))
        
        # Verificar que no existe otro SKU
        self.assertFalse(ProductRepository.sku_exists('NONEXISTENT-SKU'))
        
        # Limpiar
        product.delete()
    
    def test_get_by_category(self):
        """Test que verifica obtener productos por categoría."""
        products = ProductRepository.get_by_category(self.category.category_name)
        
        self.assertIsInstance(products, list)
        # Todos los productos deben tener la categoría correcta
        for product in products:
            self.assertEqual(product.category.category_name, self.category.category_name)


class CategoryRepositoryTest(TransactionTestCase):
    """Tests para CategoryRepository."""
    
    def setUp(self):
        """Configuración inicial para cada test."""
        # Crear las tablas necesarias para los tests
        create_test_tables()
        
        self.category = Category.objects.create(
            category_name='Test Category Repo',
            category_description='Test Description'
        )
    
    def test_get_all_categories(self):
        """Test que verifica obtener todas las categorías."""
        categories = CategoryRepository.get_all()
        
        self.assertIsInstance(categories, list)
        for category in categories:
            self.assertIsInstance(category, Category)
    
    def test_get_by_id_existing(self):
        """Test que verifica obtener una categoría por ID existente."""
        result = CategoryRepository.get_by_id(self.category.category_id)
        
        self.assertIsNotNone(result)
        self.assertEqual(result.category_id, self.category.category_id)
    
    def test_get_or_create_existing(self):
        """Test que verifica get_or_create con categoría existente."""
        # Usar first() para evitar problemas con múltiples objetos en TransactionTestCase
        existing_category = Category.objects.filter(
            category_name=self.category.category_name
        ).first()
        
        category, created = CategoryRepository.get_or_create(
            self.category.category_name
        )
        
        self.assertFalse(created)
        self.assertIsNotNone(category)
        self.assertEqual(category.category_name, self.category.category_name)
    
    def test_get_or_create_new(self):
        """Test que verifica get_or_create con categoría nueva."""
        category, created = CategoryRepository.get_or_create(
            'New Test Category',
            defaults={'category_description': 'New Description'}
        )
        
        self.assertTrue(created)
        self.assertEqual(category.category_name, 'New Test Category')
        
        # Limpiar
        category.delete()


class LicenceRepositoryTest(TransactionTestCase):
    """Tests para LicenceRepository."""
    
    def setUp(self):
        """Configuración inicial para cada test."""
        # Crear las tablas necesarias para los tests
        create_test_tables()
        
        self.licence = Licence.objects.create(
            licence_name='Test Licence Repo',
            licence_description='Test Description',
            licence_image='test.jpg'
        )
    
    def test_get_all_licences(self):
        """Test que verifica obtener todas las licencias."""
        licences = LicenceRepository.get_all()
        
        self.assertIsInstance(licences, list)
        for licence in licences:
            self.assertIsInstance(licence, Licence)
    
    def test_get_by_id_existing(self):
        """Test que verifica obtener una licencia por ID existente."""
        result = LicenceRepository.get_by_id(self.licence.licence_id)
        
        self.assertIsNotNone(result)
        self.assertEqual(result.licence_id, self.licence.licence_id)
    
    def test_get_or_create_existing(self):
        """Test que verifica get_or_create con licencia existente."""
        licence, created = LicenceRepository.get_or_create(
            self.licence.licence_name
        )
        
        self.assertFalse(created)
        self.assertIsNotNone(licence)
        self.assertEqual(licence.licence_name, self.licence.licence_name)
    
    def test_get_or_create_new(self):
        """Test que verifica get_or_create con licencia nueva."""
        licence, created = LicenceRepository.get_or_create(
            'New Test Licence',
            defaults={
                'licence_description': 'New Description',
                'licence_image': 'new.jpg'
            }
        )
        
        self.assertTrue(created)
        self.assertEqual(licence.licence_name, 'New Test Licence')
        
        # Limpiar
        licence.delete()

