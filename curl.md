# 🧪 Guía de Pruebas de API con cURL

Esta guía contiene ejemplos de cómo probar la API del backend usando `curl` desde la consola.

## 📋 Tabla de Contenidos

1. [Recomendaciones](#recomendaciones)
2. [Configuración Inicial](#configuración-inicial)
3. [Pruebas de Usuarios](#pruebas-de-usuarios)
4. [Pruebas de Productos](#pruebas-de-productos)
5. [Validación de Resultados](#validación-de-resultados)

---

## 🔧 Recomendaciones

### Para Windows (PowerShell)

1. **Usar `curl.exe` o `Invoke-RestMethod`**: PowerShell tiene un alias `curl` que puede causar problemas. Usa `curl.exe` explícitamente o mejor aún, usa `Invoke-RestMethod`.

2. **Formato JSON**: En PowerShell, usa `ConvertTo-Json` para crear el cuerpo de la petición.

3. **Comillas**: En PowerShell, usa comillas dobles `"` para strings y escapa las comillas internas con `\"`.

### Para Linux/Mac (Bash)

1. **Usar `curl` directamente**: Funciona sin problemas.

2. **Formato JSON**: Puedes escribir el JSON directamente o usar `-d @archivo.json`.

3. **Continuación de líneas**: Usa `\` al final de cada línea para comandos multilínea.

---

## ⚙️ Configuración Inicial

### URL Base
```
http://127.0.0.1:8000
```

### Headers Comunes
```
Content-Type: application/json
```

### Verificar que el servidor esté corriendo
```powershell
# PowerShell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/product/list/" -Method GET

# Bash/Linux
curl http://127.0.0.1:8000/product/list/
```

**Resultado esperado**: Lista de productos en formato JSON o error de conexión si el servidor no está corriendo.

---

## 👤 Pruebas de Usuarios

### 1. Registrar un Usuario Nuevo

#### PowerShell
```powershell
$body = @{
    name = "Jonathan"
    lastname = "Pérez"
    email = "jonathan@example.com"
    password = "miPassword123"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://127.0.0.1:8000/useraccount/register/" -Method POST -ContentType "application/json" -Body $body
```

#### Bash/Linux
```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Jonathan",
    "lastname": "Pérez",
    "email": "jonathan@example.com",
    "password": "miPassword123"
  }' \
  http://127.0.0.1:8000/useraccount/register/
```

#### Usando curl.exe en PowerShell
```powershell
curl.exe -X POST -H "Content-Type: application/json" -d "{\"name\":\"Jonathan\",\"lastname\":\"Pérez\",\"email\":\"jonathan@example.com\",\"password\":\"miPassword123\"}" http://127.0.0.1:8000/useraccount/register/
```

**Resultado esperado (201 Created)**:
```json
{
  "message": "Register successful",
  "user_id": 1,
  "email": "jonathan@example.com"
}
```

**Validación**:
- ✅ Status code: `201`
- ✅ Campo `message` contiene "Register successful"
- ✅ Campo `user_id` es un número
- ✅ Campo `email` coincide con el enviado

**Errores posibles**:
- `400`: Email ya existe, campos faltantes, validación de longitud
- `500`: Error de servidor o base de datos

---

### 2. Intentar Registrar el Mismo Usuario (Error Esperado)

#### PowerShell
```powershell
$body = @{
    name = "Jonathan"
    lastname = "Pérez"
    email = "jonathan@example.com"
    password = "miPassword123"
} | ConvertTo-Json

try {
    Invoke-RestMethod -Uri "http://127.0.0.1:8000/useraccount/register/" -Method POST -ContentType "application/json" -Body $body
} catch {
    Write-Host "Status: $($_.Exception.Response.StatusCode.value__)"
    $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
    $reader.BaseStream.Position = 0
    $reader.DiscardBufferedData()
    $responseBody = $reader.ReadToEnd()
    Write-Host $responseBody
}
```

**Resultado esperado (400 Bad Request)**:
```json
{
  "message": "Este email ya está registrado"
}
```

**Validación**:
- ✅ Status code: `400`
- ✅ Mensaje indica que el email ya existe"

---

### 3. Login de Usuario

#### PowerShell
```powershell
$body = @{
    email = "jonathan@example.com"
    password = "miPassword123"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://127.0.0.1:8000/useraccount/login/" -Method POST -ContentType "application/json" -Body $body
```

#### Bash/Linux
```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "email": "jonathan@example.com",
    "password": "miPassword123"
  }' \
  http://127.0.0.1:8000/useraccount/login/
```

**Resultado esperado (200 OK)**:
```json
{
  "message": "Login successful",
  "user_id": 1,
  "email": "jonathan@example.com",
  "name": "Jonathan"
}
```

**Validación**:
- ✅ Status code: `200`
- ✅ Campo `message` contiene "Login successful"
- ✅ Campos `user_id`, `email` y `name` presentes

**Errores posibles**:
- `400`: Campos faltantes
- `401`: Email o contraseña incorrectos

---

### 4. Login con Credenciales Incorrectas (Error Esperado)

#### PowerShell
```powershell
$body = @{
    email = "jonathan@example.com"
    password = "passwordIncorrecta"
} | ConvertTo-Json

try {
    Invoke-RestMethod -Uri "http://127.0.0.1:8000/useraccount/login/" -Method POST -ContentType "application/json" -Body $body
} catch {
    Write-Host "Status: $($_.Exception.Response.StatusCode.value__)"
    $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
    $reader.BaseStream.Position = 0
    $reader.DiscardBufferedData()
    $responseBody = $reader.ReadToEnd()
    Write-Host $responseBody
}
```

**Resultado esperado (401 Unauthorized)**:
```json
{
  "message": "Email o contraseña incorrectos"
}
```

**Validación**:
- ✅ Status code: `401`
- ✅ Mensaje indica credenciales incorrectas

---

## 📦 Pruebas de Productos

### 1. Listar Todos los Productos

#### PowerShell
```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/product/list/" -Method GET
```

#### Bash/Linux
```bash
curl http://127.0.0.1:8000/product/list/
```

**Resultado esperado (200 OK)**:
```json
[
  {
    "product_id": 1,
    "product_name": "Funko Pop! Batman",
    "product_description": "Figura coleccionable",
    "price": 5200.99,
    "stock": 10,
    "discount": 0,
    "sku": "FNK-BM-001",
    "image_front": "batman-1.webp",
    "image_back": ""
  },
  ...
]
```

**Validación**:
- ✅ Status code: `200`
- ✅ Respuesta es un array JSON
- ✅ Cada producto tiene los campos requeridos

---

### 2. Buscar Producto por ID

#### PowerShell
```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/product/find/id/1/" -Method GET
```

#### Bash/Linux
```bash
curl http://127.0.0.1:8000/product/find/id/1/
```

**Resultado esperado (200 OK)**:
```json
{
  "product_id": 1,
  "product_name": "Funko Pop! Batman",
  "product_description": "Figura coleccionable",
  "price": 5200.99,
  "stock": 10,
  "discount": 0,
  "sku": "FNK-BM-001",
  "image_front": "batman-1.webp",
  "image_back": "",
  "licence": {
    "licence_id": 1,
    "licence_name": "DC Comics"
  },
  "category": {
    "category_id": 1,
    "category_name": "Figuras"
  }
}
```

**Validación**:
- ✅ Status code: `200`
- ✅ `product_id` coincide con el buscado
- ✅ Campos `licence` y `category` presentes

---

### 3. Crear un Producto Nuevo

#### PowerShell
```powershell
$body = @{
    product_name = "Funko Pop! Superman"
    product_description = "Figura coleccionable de Superman"
    price = 5500.50
    stock = 15
    sku = "FNK-SM-001"
    discount = 10
    dues = 3
    category_name = "Figuras"
    licence_name = "DC Comics"
    image_front = "superman-1.webp"
    image_back = "superman-box.webp"
    created_by = 1
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://127.0.0.1:8000/product/create/" -Method POST -ContentType "application/json" -Body $body
```

#### Bash/Linux
```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "product_name": "Funko Pop! Superman",
    "product_description": "Figura coleccionable de Superman",
    "price": 5500.50,
    "stock": 15,
    "sku": "FNK-SM-001",
    "discount": 10,
    "dues": 3,
    "category_name": "Figuras",
    "licence_name": "DC Comics",
    "image_front": "superman-1.webp",
    "image_back": "superman-box.webp",
    "created_by": 1
  }' \
  http://127.0.0.1:8000/product/create/
```

**Resultado esperado (201 Created)**:
```json
{
  "message": "Producto creado correctamente",
  "product_id": 2,
  "product_name": "Funko Pop! Superman",
  "licence": {
    "id": 1,
    "name": "DC Comics",
    "created": false
  },
  "category": {
    "id": 1,
    "name": "Figuras",
    "created": false
  }
}
```

**Validación**:
- ✅ Status code: `201`
- ✅ Campo `message` contiene "Producto creado correctamente"
- ✅ Campo `product_id` presente
- ✅ Información de `licence` y `category` presente

**Errores posibles**:
- `400`: Campos faltantes, SKU duplicado, validación de datos
- `500`: Error de servidor o base de datos

---

### 4. Actualizar un Producto

#### PowerShell
```powershell
$body = @{
    product_name = "Funko Pop! Superman (Edición Especial)"
    product_description = "Figura coleccionable de Superman - Edición Limitada"
    price = 6000.00
    stock = 20
    discount = 15
    category_name = "Figuras"
    licence_name = "DC Comics"
    image_front = "superman-special-1.webp"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://127.0.0.1:8000/product/update/2/" -Method PUT -ContentType "application/json" -Body $body
```

#### Bash/Linux
```bash
curl -X PUT \
  -H "Content-Type: application/json" \
  -d '{
    "product_name": "Funko Pop! Superman (Edición Especial)",
    "product_description": "Figura coleccionable de Superman - Edición Limitada",
    "price": 6000.00,
    "stock": 20,
    "discount": 15,
    "category_name": "Figuras",
    "licence_name": "DC Comics",
    "image_front": "superman-special-1.webp"
  }' \
  http://127.0.0.1:8000/product/update/2/
```

**Resultado esperado (200 OK)**:
```json
{
  "message": "Producto actualizado correctamente",
  "product_id": 2,
  "product_name": "Funko Pop! Superman (Edición Especial)"
}
```

**Validación**:
- ✅ Status code: `200`
- ✅ Campo `message` contiene "Producto actualizado correctamente"
- ✅ `product_id` coincide con el actualizado

---

### 5. Eliminar un Producto

#### PowerShell
```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/product/delete/2/" -Method DELETE
```

#### Bash/Linux
```bash
curl -X DELETE http://127.0.0.1:8000/product/delete/2/
```

**Resultado esperado (200 OK)**:
```json
{
  "message": "Producto eliminado correctamente",
  "product_id": 2,
  "product_name": "Funko Pop! Superman (Edición Especial)"
}
```

**Validación**:
- ✅ Status code: `200`
- ✅ Campo `message` contiene "Producto eliminado correctamente"
- ✅ Información del producto eliminado presente

---

### 6. Listar Categorías

#### PowerShell
```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/category/" -Method GET
```

#### Bash/Linux
```bash
curl http://127.0.0.1:8000/category/
```

**Resultado esperado (200 OK)**:
```json
[
  {
    "category_id": 1,
    "category_name": "Figuras",
    "category_description": "Figuras coleccionables",
    "image_category": null
  },
  ...
]
```

---

### 7. Listar Licencias

#### PowerShell
```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/licence/" -Method GET
```

#### Bash/Linux
```bash
curl http://127.0.0.1:8000/licence/
```

**Resultado esperado (200 OK)**:
```json
[
  {
    "licence_id": 1,
    "licence_name": "DC Comics",
    "licence_description": "Licencia de DC Comics",
    "licence_image": null
  },
  ...
]
```

---

## ✅ Validación de Resultados

### Métodos de Validación

#### 1. Verificar Status Code

**PowerShell**:
```powershell
try {
    $response = Invoke-RestMethod -Uri "..." -Method POST -Body $body
    Write-Host "✅ Éxito - Status: 200/201"
} catch {
    $statusCode = $_.Exception.Response.StatusCode.value__
    Write-Host "❌ Error - Status: $statusCode"
}
```

**Bash/Linux**:
```bash
curl -w "\nHTTP Status: %{http_code}\n" -X POST ...
```

#### 2. Verificar Estructura JSON

**PowerShell**:
```powershell
$response = Invoke-RestMethod -Uri "..." -Method GET
if ($response.message) {
    Write-Host "✅ Campo 'message' presente: $($response.message)"
}
if ($response.product_id) {
    Write-Host "✅ Campo 'product_id' presente: $($response.product_id)"
}
```

#### 3. Validar Contenido Específico

**PowerShell**:
```powershell
$response = Invoke-RestMethod -Uri "..." -Method POST -Body $body

# Validar que el registro fue exitoso
if ($response.message -eq "Register successful") {
    Write-Host "✅ Usuario registrado correctamente"
    Write-Host "   User ID: $($response.user_id)"
    Write-Host "   Email: $($response.email)"
} else {
    Write-Host "❌ Error: $($response.message)"
}
```

#### 4. Guardar Respuesta en Archivo

**PowerShell**:
```powershell
$response = Invoke-RestMethod -Uri "..." -Method GET
$response | ConvertTo-Json -Depth 10 | Out-File -FilePath "response.json" -Encoding UTF8
```

**Bash/Linux**:
```bash
curl http://127.0.0.1:8000/product/list/ > response.json
```

#### 5. Validar con jq (Bash/Linux)

Si tienes `jq` instalado:
```bash
curl http://127.0.0.1:8000/product/list/ | jq '.[0].product_name'
```

---

## 🧪 Script de Pruebas Completo (PowerShell)

Crea un archivo `test-api.ps1`:

```powershell
# Script de Pruebas de API
$baseUrl = "http://127.0.0.1:8000"

Write-Host "=== PRUEBAS DE API ===" -ForegroundColor Cyan

# 1. Registrar Usuario
Write-Host "`n1. Registrando usuario..." -ForegroundColor Yellow
$registerBody = @{
    name = "TestUser"
    lastname = "Test"
    email = "test@example.com"
    password = "test123"
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri "$baseUrl/useraccount/register/" -Method POST -ContentType "application/json" -Body $registerBody
    Write-Host "✅ Usuario registrado - ID: $($response.user_id)" -ForegroundColor Green
} catch {
    Write-Host "❌ Error: $($_.Exception.Message)" -ForegroundColor Red
}

# 2. Login
Write-Host "`n2. Login..." -ForegroundColor Yellow
$loginBody = @{
    email = "test@example.com"
    password = "test123"
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri "$baseUrl/useraccount/login/" -Method POST -ContentType "application/json" -Body $loginBody
    Write-Host "✅ Login exitoso - Usuario: $($response.name)" -ForegroundColor Green
} catch {
    Write-Host "❌ Error: $($_.Exception.Message)" -ForegroundColor Red
}

# 3. Listar Productos
Write-Host "`n3. Listando productos..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "$baseUrl/product/list/" -Method GET
    Write-Host "✅ Productos encontrados: $($response.Count)" -ForegroundColor Green
} catch {
    Write-Host "❌ Error: $($_.Exception.Message)" -ForegroundColor Red
}

# 4. Crear Producto
Write-Host "`n4. Creando producto..." -ForegroundColor Yellow
$productBody = @{
    product_name = "Funko Pop! Test"
    product_description = "Producto de prueba"
    price = 1000.00
    stock = 5
    sku = "TEST-001"
    discount = 0
    category_name = "Figuras"
    licence_name = "DC Comics"
    image_front = "test.webp"
    created_by = 1
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri "$baseUrl/product/create/" -Method POST -ContentType "application/json" -Body $productBody
    Write-Host "✅ Producto creado - ID: $($response.product_id)" -ForegroundColor Green
    $productId = $response.product_id
} catch {
    Write-Host "❌ Error: $($_.Exception.Message)" -ForegroundColor Red
    $productId = $null
}

# 5. Buscar Producto por ID
if ($productId) {
    Write-Host "`n5. Buscando producto ID: $productId..." -ForegroundColor Yellow
    try {
        $response = Invoke-RestMethod -Uri "$baseUrl/product/find/id/$productId/" -Method GET
        Write-Host "✅ Producto encontrado: $($response.product_name)" -ForegroundColor Green
    } catch {
        Write-Host "❌ Error: $($_.Exception.Message)" -ForegroundColor Red
    }
}

Write-Host "`n=== PRUEBAS COMPLETADAS ===" -ForegroundColor Cyan
```

Ejecuta el script:
```powershell
.\test-api.ps1
```

---

## 📝 Notas Importantes

1. **CSRF Deshabilitado**: Las vistas tienen `@csrf_exempt`, por lo que no necesitas tokens CSRF.

2. **Formato de Respuesta**: Todas las respuestas son JSON.

3. **Códigos de Estado HTTP**:
   - `200`: Éxito (GET, PUT)
   - `201`: Creado (POST)
   - `400`: Error de validación
   - `401`: No autorizado
   - `404`: No encontrado
   - `405`: Método no permitido
   - `500`: Error del servidor

4. **Validación de Campos**: El backend valida:
   - Campos requeridos
   - Longitud máxima de campos
   - Formato de email
   - Unicidad de email y SKU

5. **Base de Datos**: Los cambios se guardan en `db.sqlite3`.

---

## 🔍 Troubleshooting

### Error: "No se puede conectar al servidor"
- Verifica que el servidor Django esté corriendo: `python manage.py runserver`
- Verifica que la URL sea correcta: `http://127.0.0.1:8000`

### Error: "JSON inválido"
- Verifica que el JSON esté bien formateado
- Usa `ConvertTo-Json` en PowerShell o valida el JSON antes de enviarlo

### Error: "403 Forbidden"
- Verifica que las vistas tengan `@csrf_exempt`
- Reinicia el servidor Django después de cambios

### Error: "500 Internal Server Error"
- Revisa los logs del servidor Django
- Verifica que la base de datos esté accesible
- Verifica que los modelos estén correctamente configurados

---

## 📚 Referencias

- [Documentación de cURL](https://curl.se/docs/)
- [PowerShell Invoke-RestMethod](https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/invoke-restmethod)
- [Django REST Framework](https://www.django-rest-framework.org/)

