# 🛒 Proyecto Ecommerce - Shop

Sistema de comercio electrónico desarrollado con Django 5.2.8 que gestiona productos, categorías, licencias y cuentas de usuario.

## 📋 Tabla de Contenidos

1. [Instalación](#instalación)
2. [Inicialización](#inicialización)
3. [Estructura del Proyecto](#estructura-del-proyecto)
4. [Servicios Creados](#servicios-creados)
5. [Avances](#avances)

---

## 🔧 Instalación

### Requisitos Previos

- Python 3.8 o superior
- MySQL (base de datos en la nube)
- pip (gestor de paquetes de Python)

### Pasos de Instalación

1. **Clonar o descargar el proyecto**
   ```bash
   cd Shop
   ```

2. **Crear un entorno virtual (recomendado)**
   ```bash
   # Windows
   python -m venv venv
   
   # Linux/Mac
   python3 -m venv venv
   ```

3. **Activar el entorno virtual**
   ```bash
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

4. **Instalar las dependencias**
   ```bash
   pip install -r requirements.txt
   ```

   Las dependencias incluyen:
   - Django>=5.2.8
   - python-decouple>=3.8
   - PyMySQL>=1.1.0

5. **Configurar variables de entorno**

   Crea un archivo `.env` en la raíz del proyecto con las siguientes variables:
   ```env
   SECRET_KEY=tu-clave-secreta-aqui
   DB_NAME=funkotest_funkos
   DB_USER=funkotest
   DB_PASS=tu-contraseña
   DB_HOST=mysql-funkotest.alwaysdata.net
   DB_PORT=3306
   ```

   **Nota:** Si no creas el archivo `.env`, el proyecto usará valores por defecto (no recomendado para producción).

---

## 🚀 Inicialización

### 1. Verificar la conexión a la base de datos

La aplicación está configurada para conectarse a una base de datos MySQL en la nube. Asegúrate de que las credenciales en tu archivo `.env` sean correctas.

### 2. Ejecutar migraciones (si es necesario)

```bash
python manage.py makemigrations
python manage.py migrate
```

**Nota:** Los modelos tienen `managed = False`, lo que significa que las tablas ya existen en la base de datos y Django no las gestiona automáticamente.

### 3. Crear un superusuario (opcional)

```bash
python manage.py createsuperuser
```

### 4. Iniciar el servidor de desarrollo

```bash
python manage.py runserver
```

O para acceder desde otras máquinas en la red local:

```bash
python manage.py runserver 0.0.0.0:8000
```

### 5. Acceder a la aplicación

- **API Base:** `http://localhost:8000/` o `http://127.0.0.1:8000/`
- **Panel de Administración:** `http://localhost:8000/admin/`
- **Desde la red local:** `http://192.168.2.5:8000` o `http://192.168.0.15:8000`

---

## 📁 Estructura del Proyecto

```
Shop/
│
├── Ecommerce/                  # Configuración principal del proyecto
│   ├── __init__.py
│   ├── settings.py            # Configuración de Django
│   ├── urls.py                # URLs principales
│   ├── wsgi.py                # Configuración WSGI
│   └── asgi.py                # Configuración ASGI
│
├── totalisting/                # App para gestión de productos
│   ├── __init__.py
│   ├── models.py              # Modelos: Product, Category, Licence
│   ├── views.py               # Vistas CRUD completas
│   ├── urls.py                # Rutas de la API de productos
│   ├── admin.py               # Configuración del admin
│   └── migrations/            # Migraciones de base de datos
│
├── useraccount/                # App para gestión de usuarios
│   ├── __init__.py
│   ├── models.py              # Modelos: User, Role
│   ├── views.py               # Vistas de autenticación y perfil
│   ├── urls.py                # Rutas de la API de usuarios
│   ├── admin.py
│   └── migrations/
│
├── buyingflow/                 # App para flujo de compra (en desarrollo)
│   ├── __init__.py
│   ├── models.py
│   ├── views.py
│   └── migrations/
│
├── manage.py                   # Script de gestión de Django
├── requirements.txt            # Dependencias del proyecto
├── db.sqlite3                  # Base de datos SQLite (si se usa)
└── README.md                   # Este archivo
```

### Descripción de Apps

- **Ecommerce:** Configuración principal del proyecto Django
- **totalisting:** Gestión completa de productos, categorías y licencias (CRUD completo)
- **useraccount:** Sistema de autenticación y gestión de perfiles de usuario
- **buyingflow:** Flujo de compra (pendiente de implementación)

---

## 🔌 Servicios Creados

### 📦 API de Productos (`totalisting`)

#### CREATE (Crear)
- `POST /product/create/` - Crear un nuevo producto
  - Crea automáticamente licencias y categorías si no existen
  - Valida SKU único

#### READ (Leer)

**Categorías:**
- `GET /category/` - Lista todas las categorías
- `GET /category/by-license/<license_name>/` - Categorías filtradas por licencia
- `GET /category/<category_name>/` - Vista de categoría específica

**Licencias:**
- `GET /licence/` - Lista todas las licencias
- `GET /licence/<license_name>/` - Licencias filtradas por nombre

**Productos:**
- `GET /product/list/` - Lista todos los productos
- `GET /product/list/category/<category_name>/` - Productos por categoría
- `GET /product/list/license/<license_name>/` - Productos por licencia
- `GET /product/<product_name>/` - Vista de producto
- `GET /product/find/id/<product_id>/` - Buscar producto por ID
- `GET /product/find/name/<product_name>/` - Buscar producto por nombre
- `GET /product/find/sku/<sku>/` - Buscar producto por SKU

#### UPDATE (Actualizar)
- `PUT/POST /product/update/<product_id>/` - Actualizar producto
- `PUT/POST /category/update/<category_id>/` - Actualizar categoría
- `PUT/POST /licence/update/<licence_id>/` - Actualizar licencia

#### DELETE (Eliminar)
- `DELETE/POST /product/delete/<product_id>/` - Eliminar producto
- `DELETE/POST /category/delete/<category_id>/` - Eliminar categoría (con validación de productos asociados)
- `DELETE/POST /licence/delete/<licence_id>/` - Eliminar licencia (con validación de productos asociados)

### 👤 API de Usuarios (`useraccount`)

#### Autenticación
- `POST /useraccount/login/` - Iniciar sesión
- `POST /useraccount/register/` - Registrar nuevo usuario
- `POST /useraccount/logout/` - Cerrar sesión

#### Perfil de Usuario
- `GET /useraccount/profile/` - Obtener perfil del usuario
- `POST /useraccount/profile/edit/` - Editar perfil
- `POST /useraccount/profile/delete/` - Eliminar cuenta

#### Configuración de Perfil
- `POST /useraccount/profile/change-password/` - Cambiar contraseña
- `POST /useraccount/profile/change-email/` - Cambiar email
- `POST /useraccount/profile/change-username/` - Cambiar nombre de usuario
- `POST /useraccount/profile/change-avatar/` - Cambiar avatar
- `POST /useraccount/profile/change-background/` - Cambiar fondo
- `POST /useraccount/profile/change-theme/` - Cambiar tema
- `POST /useraccount/profile/change-language/` - Cambiar idioma

---

## 📈 Avances

### ✅ Completado

#### Configuración del Proyecto
- [x] Configuración inicial de Django 5.2.8
- [x] Conexión a base de datos MySQL en la nube
- [x] Configuración de variables de entorno con `python-decouple`
- [x] Configuración de IPs para acceso en red local
- [x] Estructura de apps modular

#### Modelos de Datos
- [x] Modelo `Product` con relaciones a Category y Licence
- [x] Modelo `Category` para categorías de productos
- [x] Modelo `Licence` para licencias de productos
- [x] Modelo `User` para usuarios del sistema
- [x] Modelo `Role` para roles de usuario
- [x] Configuración de modelos con `managed = False` (tablas existentes)

#### API de Productos (CRUD Completo)
- [x] **CREATE:** Crear productos con creación automática de licencias/categorías
- [x] **READ:** 
  - Listado de productos, categorías y licencias
  - Filtrado por categoría y licencia
  - Búsqueda por ID, nombre y SKU
- [x] **UPDATE:** Actualización de productos, categorías y licencias
- [x] **DELETE:** Eliminación con validación de integridad referencial

#### API de Usuarios
- [x] Sistema de autenticación (login, registro, logout)
- [x] Gestión de perfiles de usuario
- [x] Funciones de cambio de configuración de perfil

#### Correcciones y Mejoras
- [x] Corrección de errores en funciones de búsqueda
- [x] Validación de datos en todas las operaciones
- [x] Manejo de errores con mensajes descriptivos
- [x] Organización del código por operaciones CRUD
- [x] Documentación de funciones

### 🚧 En Desarrollo

- [ ] App `buyingflow` - Flujo de compra
- [ ] Sistema de carrito de compras
- [ ] Procesamiento de pagos
- [ ] Gestión de pedidos

### 📝 Pendiente

- [ ] Tests unitarios y de integración
- [ ] Documentación de API con Swagger/OpenAPI
- [ ] Autenticación con tokens JWT
- [ ] Sistema de permisos y roles
- [ ] Upload de imágenes para productos
- [ ] Sistema de búsqueda avanzada
- [ ] Filtros y paginación en listados
- [ ] Cache para mejorar rendimiento
- [ ] Logging y monitoreo

---

## 🛠️ Tecnologías Utilizadas

- **Backend:** Django 5.2.8
- **Base de Datos:** MySQL (en la nube)
- **ORM:** Django ORM
- **Autenticación:** Django Sessions
- **Configuración:** python-decouple
- **Driver MySQL:** PyMySQL

---

## 📝 Notas Importantes

1. **Base de Datos:** Los modelos están configurados con `managed = False` porque las tablas ya existen en la base de datos. Django no creará ni modificará estas tablas automáticamente.

2. **Seguridad:** El proyecto está en modo desarrollo (`DEBUG = True`). Para producción, asegúrate de:
   - Cambiar `DEBUG = False`
   - Configurar `ALLOWED_HOSTS` apropiadamente
   - Usar una clave secreta segura
   - Configurar HTTPS

3. **Variables de Entorno:** Nunca subas el archivo `.env` al repositorio. Usa valores por defecto solo para desarrollo local.

---

## 👥 Contribuidores

- Desarrollado para IFTS4 - Desarrollo de Software

---

## 📄 Licencia

Este proyecto es parte de un trabajo académico.

---

## 📞 Soporte

Para consultas o problemas, contacta al equipo de desarrollo.

---

**Última actualización:** 2025

