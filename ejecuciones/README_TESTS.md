# Guía de Tests Unitarios

## Estructura de Tests

Los tests están organizados en el directorio `totalisting/tests/`:

- `test_serializers.py`: Tests para serializers (ProductSerializer, CategorySerializer, LicenceSerializer)
- `test_repositories.py`: Tests para repositorios (ProductRepository, CategoryRepository, LicenceRepository)
- `test_services.py`: Tests para servicios (ProductService, CategoryService, LicenceService)
- `test_factories.py`: Tests para factories (ProductFactory)

## Ejecutar Tests

### Opción 1: Usando Django TestCase
```bash
python manage.py test totalisting.tests
```

### Opción 2: Ejecutar tests específicos
```bash
# Solo tests de serializers
python manage.py test totalisting.tests.test_serializers

# Solo tests de servicios
python manage.py test totalisting.tests.test_services

# Solo un test específico
python manage.py test totalisting.tests.test_services.ProductServiceTest.test_create_product_success
```

### Opción 3: Con más verbosidad
```bash
python manage.py test totalisting.tests --verbosity=2
```

### Opción 4: Con cobertura (si tienes coverage instalado)
```bash
coverage run --source='totalisting' manage.py test totalisting.tests
coverage report
coverage html
```

## Buenas Prácticas Implementadas

1. **Separación por módulos**: Cada componente tiene su propio archivo de tests
2. **setUp y tearDown**: Cada test class tiene setUp para datos de prueba
3. **Nombres descriptivos**: Los nombres de los tests describen qué prueban
4. **Una aserción por concepto**: Cada test verifica un comportamiento específico
5. **Tests independientes**: Cada test puede ejecutarse de forma independiente
6. **Limpieza de datos**: Los tests limpian los datos que crean

## Notas Importantes

- Los modelos tienen `managed = False`, por lo que las tablas deben existir en la BD
- Los tests crean y eliminan datos de prueba automáticamente
- Algunos tests pueden fallar si la base de datos no tiene las tablas creadas

## Cobertura de Tests

Los tests cubren:
- ✅ Serialización de modelos a JSON
- ✅ Validación de datos de entrada
- ✅ Operaciones CRUD en repositorios
- ✅ Lógica de negocio en servicios
- ✅ Creación de objetos complejos en factories
- ✅ Manejo de errores y casos límite

