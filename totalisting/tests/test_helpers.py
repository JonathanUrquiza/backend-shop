"""
Helpers para tests que requieren creación de tablas.

Como los modelos tienen managed=False, necesitamos crear las tablas manualmente.
"""

from django.db import connection


def create_test_tables():
    """
    Crea las tablas necesarias para los tests.
    
    Como los modelos tienen managed=False, Django no crea las tablas automáticamente.
    Esta función crea las tablas usando SQL directo.
    """
    with connection.cursor() as cursor:
        # Crear tabla licence
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS licence (
                licence_id INTEGER PRIMARY KEY AUTOINCREMENT,
                licence_name VARCHAR(45) NOT NULL,
                licence_description VARCHAR(255) NOT NULL,
                licence_image VARCHAR(255)
            )
        """)
        
        # Crear tabla category
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS category (
                category_id INTEGER PRIMARY KEY AUTOINCREMENT,
                category_name VARCHAR(100) NOT NULL,
                category_description VARCHAR(255)
            )
        """)
        
        # Crear tabla product
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS product (
                product_id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_name VARCHAR(60) NOT NULL,
                product_description VARCHAR(255) NOT NULL,
                price DECIMAL(10, 2) NOT NULL,
                stock INTEGER NOT NULL,
                discount INTEGER,
                sku VARCHAR(30) NOT NULL UNIQUE,
                dues INTEGER,
                created_by INTEGER NOT NULL,
                image_front VARCHAR(200) NOT NULL,
                image_back VARCHAR(200) NOT NULL,
                create_time DATETIME,
                licence_id INTEGER NOT NULL,
                category_id INTEGER NOT NULL,
                FOREIGN KEY (licence_id) REFERENCES licence(licence_id),
                FOREIGN KEY (category_id) REFERENCES category(category_id)
            )
        """)
        
        # Crear índices para mejorar rendimiento
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_product_licence ON product(licence_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_product_category ON product(category_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_product_sku ON product(sku)")


def drop_test_tables():
    """
    Elimina las tablas de prueba.
    
    Útil para limpiar después de los tests.
    """
    with connection.cursor() as cursor:
        cursor.execute("DROP TABLE IF EXISTS product")
        cursor.execute("DROP TABLE IF EXISTS category")
        cursor.execute("DROP TABLE IF EXISTS licence")

