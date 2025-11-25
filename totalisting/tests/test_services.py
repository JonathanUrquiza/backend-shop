"""
Tests unitarios para los servicios.

Prueba la lógica de negocio encapsulada en los servicios.
"""

from django.test import TestCase, TransactionTestCase
from totalisting.models import Product, Category, Licence
from totalisting.services import (
    ProductService,
    CategoryService,
    LicenceService
)
from .test_helpers import create_test_tables


class ProductServiceTest(TransactionTestCase):
    """Tests para ProductService."""
    
    def setUp(self):
        """Configuración inicial para cada test."""
        # Crear las tablas necesarias para los tests
        create_test_tables()
        
        # Crear licencia de prueba
        self.licence = Licence.objects.create(
            licence_name='Test Licence Service',
            licence_description='Test Description',
            licence_image='test.jpg'
        )
        
        # Crear categoría de prueba
        self.category = Category.objects.create(
            category_name='Test Category Service',
            category_description='Test Description'
        )
    
    def test_get_all_products(self):
        """Test que verifica obtener todos los productos."""
        products = ProductService.get_all_products()
        
        self.assertIsInstance(products, list)
        # Verificar estructura de datos
        if products:
            self.assertIn('product_id', products[0])
            self.assertIn('product_name', products[0])
            self.assertIn('price', products[0])
    
    def test_get_product_by_id_existing(self):
        """Test que verifica obtener un producto por ID existente."""
        # Crear producto de prueba
        product = Product.objects.create(
            product_name='Test Product Service',
            product_description='Test',
            price=99.99,
            stock=10,
            sku='TEST-SERVICE-001',
            licence=self.licence,
            category=self.category,
            created_by=1,
            image_front='',
            image_back=''
        )
        
        product_data, error = ProductService.get_product_by_id(product.product_id)
        
        self.assertIsNotNone(product_data)
        self.assertIsNone(error)
        self.assertEqual(product_data['product_id'], product.product_id)
        self.assertEqual(product_data['product_name'], 'Test Product Service')
        self.assertIn('licence', product_data)
        self.assertIn('category', product_data)
        
        # Limpiar
        product.delete()
    
    def test_get_product_by_id_nonexistent(self):
        """Test que verifica obtener un producto por ID inexistente."""
        product_data, error = ProductService.get_product_by_id(99999)
        
        self.assertIsNone(product_data)
        self.assertIsNotNone(error)
        self.assertEqual(error, 'Producto no encontrado')
    
    def test_get_product_by_sku_existing(self):
        """Test que verifica obtener un producto por SKU existente."""
        # Crear producto de prueba
        product = Product.objects.create(
            product_name='Test Product SKU Service',
            product_description='Test',
            price=99.99,
            stock=10,
            sku='TEST-SERVICE-SKU-001',
            licence=self.licence,
            category=self.category,
            created_by=1,
            image_front='',
            image_back=''
        )
        
        product_data, error = ProductService.get_product_by_sku('TEST-SERVICE-SKU-001')
        
        self.assertIsNotNone(product_data)
        self.assertIsNone(error)
        self.assertEqual(product_data['sku'], 'TEST-SERVICE-SKU-001')
        
        # Limpiar
        product.delete()
    
    def test_get_products_by_category(self):
        """Test que verifica obtener productos por categoría."""
        products = ProductService.get_products_by_category(self.category.category_name)
        
        self.assertIsInstance(products, list)
        # Todos deben tener la categoría correcta
        for product_data in products:
            self.assertIn('product_id', product_data)
            self.assertIn('product_name', product_data)
    
    def test_create_product_success(self):
        """Test que verifica la creación exitosa de un producto."""
        data = {
            'product_name': 'New Product Service',
            'product_description': 'New Description',
            'price': '50.00',
            'stock': '5',
            'sku': 'NEW-SERVICE-001',
            'licence': 'Test Licence Service',
            'category': 'Test Category Service'
        }
        
        product, error, metadata = ProductService.create_product(data)
        
        self.assertIsNotNone(product)
        self.assertIsNone(error)
        self.assertEqual(product.product_name, 'New Product Service')
        self.assertIn('licence', metadata)
        self.assertIn('category', metadata)
        
        # Limpiar
        product.delete()
    
    def test_create_product_duplicate_sku(self):
        """Test que verifica la creación fallida por SKU duplicado."""
        # Crear producto primero
        product = Product.objects.create(
            product_name='Existing Product',
            product_description='Test',
            price=99.99,
            stock=10,
            sku='DUPLICATE-SKU-001',
            licence=self.licence,
            category=self.category,
            created_by=1,
            image_front='',
            image_back=''
        )
        
        # Intentar crear otro con el mismo SKU
        data = {
            'product_name': 'Duplicate Product',
            'product_description': 'Test',
            'price': '50.00',
            'stock': '5',
            'sku': 'DUPLICATE-SKU-001',
            'licence': 'Test Licence Service',
            'category': 'Test Category Service'
        }
        
        new_product, error, metadata = ProductService.create_product(data)
        
        self.assertIsNone(new_product)
        self.assertIsNotNone(error)
        self.assertIn('SKU', error)
        
        # Limpiar
        product.delete()
    
    def test_update_product_success(self):
        """Test que verifica la actualización exitosa de un producto."""
        # Crear producto
        product = Product.objects.create(
            product_name='Product To Update',
            product_description='Original',
            price=99.99,
            stock=10,
            sku='UPDATE-SERVICE-001',
            licence=self.licence,
            category=self.category,
            created_by=1,
            image_front='',
            image_back=''
        )
        
        # Actualizar
        data = {
            'product_name': 'Updated Product',
            'price': '150.00',
            'stock': '20'
        }
        
        updated_product, error = ProductService.update_product(product.product_id, data)
        
        self.assertIsNotNone(updated_product)
        self.assertIsNone(error)
        self.assertEqual(updated_product.product_name, 'Updated Product')
        self.assertEqual(float(updated_product.price), 150.00)
        self.assertEqual(updated_product.stock, 20)
        
        # Limpiar
        updated_product.delete()
    
    def test_delete_product_success(self):
        """Test que verifica la eliminación exitosa de un producto."""
        # Crear producto
        product = Product.objects.create(
            product_name='Product To Delete',
            product_description='Test',
            price=99.99,
            stock=10,
            sku='DELETE-SERVICE-001',
            licence=self.licence,
            category=self.category,
            created_by=1,
            image_front='',
            image_back=''
        )
        
        product_id = product.product_id
        
        # Eliminar
        success, error, product_data = ProductService.delete_product(product_id)
        
        self.assertTrue(success)
        self.assertIsNone(error)
        self.assertIsNotNone(product_data)
        self.assertEqual(product_data['product_id'], product_id)
        
        # Verificar que fue eliminado
        self.assertFalse(Product.objects.filter(product_id=product_id).exists())


class CategoryServiceTest(TransactionTestCase):
    """Tests para CategoryService."""
    
    def setUp(self):
        """Configuración inicial para cada test."""
        # Crear las tablas necesarias para los tests
        create_test_tables()
        
        self.category = Category.objects.create(
            category_name='Test Category Service',
            category_description='Test Description'
        )
    
    def test_get_all_categories(self):
        """Test que verifica obtener todas las categorías."""
        categories = CategoryService.get_all_categories()
        
        self.assertIsInstance(categories, list)
        if categories:
            self.assertIn('category_id', categories[0])
            self.assertIn('category_name', categories[0])
    
    def test_update_category_success(self):
        """Test que verifica la actualización exitosa de una categoría."""
        data = {
            'category_name': 'Updated Category',
            'category_description': 'Updated Description'
        }
        
        updated_category, error = CategoryService.update_category(
            self.category.category_id,
            data
        )
        
        self.assertIsNotNone(updated_category)
        self.assertIsNone(error)
        self.assertEqual(updated_category.category_name, 'Updated Category')
        
        # Restaurar
        self.category.category_name = 'Test Category Service'
        self.category.save()
    
    def test_delete_category_without_products(self):
        """Test que verifica la eliminación de una categoría sin productos."""
        # Crear categoría sin productos
        category = Category.objects.create(
            category_name='Category To Delete',
            category_description='Test'
        )
        
        category_id = category.category_id
        
        # Eliminar
        success, error, category_data = CategoryService.delete_category(category_id)
        
        self.assertTrue(success)
        self.assertIsNone(error)
        self.assertIsNotNone(category_data)


class LicenceServiceTest(TransactionTestCase):
    """Tests para LicenceService."""
    
    def setUp(self):
        """Configuración inicial para cada test."""
        # Crear las tablas necesarias para los tests
        create_test_tables()
        
        self.licence = Licence.objects.create(
            licence_name='Test Licence Service',
            licence_description='Test Description',
            licence_image='test.jpg'
        )
    
    def test_get_all_licences(self):
        """Test que verifica obtener todas las licencias."""
        licences = LicenceService.get_all_licences()
        
        self.assertIsInstance(licences, list)
        if licences:
            self.assertIn('licence_id', licences[0])
            self.assertIn('licence_name', licences[0])
    
    def test_update_licence_success(self):
        """Test que verifica la actualización exitosa de una licencia."""
        data = {
            'licence_name': 'Updated Licence',
            'licence_description': 'Updated Description'
        }
        
        updated_licence, error = LicenceService.update_licence(
            self.licence.licence_id,
            data
        )
        
        self.assertIsNotNone(updated_licence)
        self.assertIsNone(error)
        self.assertEqual(updated_licence.licence_name, 'Updated Licence')
        
        # Restaurar
        self.licence.licence_name = 'Test Licence Service'
        self.licence.save()

