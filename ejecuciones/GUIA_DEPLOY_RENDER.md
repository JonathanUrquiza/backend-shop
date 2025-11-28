# Guía de Despliegue en Render

## 📋 Archivos Creados para Render

### 1. Procfile
Archivo que le dice a Render cómo ejecutar la aplicación.

### 2. build.sh
Script de construcción que se ejecuta antes del despliegue.

### 3. requirements.txt (actualizado)
Incluye `gunicorn` y `whitenoise` necesarios para producción.

### 4. settings.py (actualizado)
- Configuración de DEBUG desde variables de entorno
- ALLOWED_HOSTS dinámico
- Configuración de archivos estáticos con WhiteNoise

---

## 🚀 Pasos para Desplegar en Render

### Paso 1: Preparar el Repositorio

1. Asegúrate de que todos los cambios estén en Git:
```bash
git add .
git commit -m "Preparación para despliegue en Render"
git push origin main
```

### Paso 2: Crear Servicio en Render

1. Ve a [render.com](https://render.com) y crea una cuenta
2. Haz clic en **"New +"** → **"Web Service"**
3. Conecta tu repositorio (GitHub/GitLab/Bitbucket)

### Paso 3: Configurar el Servicio

**Configuración básica:**
- **Name**: `ecommerce-shop` (o el nombre que prefieras)
- **Environment**: `Python 3`
- **Build Command**: `./build.sh` o `pip install -r requirements.txt && python manage.py collectstatic --no-input`
- **Start Command**: `gunicorn Ecommerce.wsgi:application`

### Paso 4: Configurar Variables de Entorno (Primera Vez)

En la sección **"Environment Variables"** de Render, agrega estas variables **SIN el dominio todavía**:

```
SECRET_KEY=tu-clave-secreta-muy-segura-aqui
DEBUG=False
DB_NAME=funkotest_funkos
DB_USER=funkotest
DB_PASS=tu-password-de-base-de-datos
DB_HOST=mysql-funkotest.alwaysdata.net
DB_PORT=3306
ALLOWED_HOSTS=localhost,127.0.0.1
```

**⚠️ IMPORTANTE:**
- Usa una `SECRET_KEY` segura (puedes generar una con: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`)
- Por ahora deja `ALLOWED_HOSTS` sin el dominio de Render (lo agregaremos después)

### Paso 4.5: Obtener el Dominio de Render y Actualizar Variables

**Después de crear el servicio:**

1. **Espera a que Render termine de desplegar** (puede tardar varios minutos)
2. Una vez desplegado, Render te asignará un dominio automáticamente
3. **Encuentra tu dominio:**
   - Ve a tu servicio en Render
   - En la parte superior verás algo como: `https://tu-app-xxxx.onrender.com`
   - O ve a **Settings** → **Domains** para ver el dominio asignado

4. **Actualiza la variable de entorno `ALLOWED_HOSTS`:**
   - Ve a **Environment** en tu servicio de Render
   - Busca la variable `ALLOWED_HOSTS`
   - Edítala y agrega el dominio de Render:
   ```
   ALLOWED_HOSTS=tu-app-xxxx.onrender.com,localhost,127.0.0.1
   ```
   - Reemplaza `tu-app-xxxx.onrender.com` con el dominio real que Render te asignó
   - Haz clic en **Save Changes**

5. **Render reiniciará automáticamente** tu servicio con la nueva configuración

**Ejemplo:**
Si tu dominio es `https://ecommerce-shop-abc123.onrender.com`, entonces:
```
ALLOWED_HOSTS=ecommerce-shop-abc123.onrender.com,localhost,127.0.0.1
```

### Paso 5: Obtener Dominio y Actualizar ALLOWED_HOSTS

**IMPORTANTE:** Render asigna el dominio **después** de crear el servicio.

1. **Espera a que Render termine de desplegar** (puede tardar varios minutos)
2. **Encuentra tu dominio:**
   - Ve a tu servicio → Verás el dominio en la parte superior
   - O ve a **Settings** → **Domains**
   - Ejemplo: `https://tu-app-xxxx.onrender.com`

3. **Actualiza `ALLOWED_HOSTS`:**
   - Ve a **Environment** en tu servicio
   - Busca `ALLOWED_HOSTS`
   - Edítala y agrega el dominio: `tu-app-xxxx.onrender.com,localhost,127.0.0.1`
   - Solo el nombre del dominio, SIN `https://` y SIN `/`
   - Guarda los cambios

4. Render reiniciará automáticamente con la nueva configuración

📖 **Ver guía detallada:** `ejecuciones/INSTRUCCIONES_DOMINIO_RENDER.md`

### Paso 6: Configurar Base de Datos (Opcional)

Si quieres usar una base de datos de Render en lugar de la externa:

1. Crea una base de datos PostgreSQL en Render
2. Actualiza las variables de entorno:
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=nombre_bd_render
DB_USER=usuario_render
DB_PASS=password_render
DB_HOST=host_render
DB_PORT=5432
```

### Paso 7: Desplegar

1. Haz clic en **"Create Web Service"**
2. Render comenzará a construir y desplegar tu aplicación
3. Espera a que termine el proceso (puede tardar varios minutos)

---

## 🔧 Configuraciones Adicionales Recomendadas

### Health Check (Opcional)

Crea un endpoint simple para verificar que la app está funcionando:

```python
# En totalisting/views.py o crear un nuevo archivo
from django.http import JsonResponse

def health_check(request):
    return JsonResponse({'status': 'ok'})
```

Y agrégalo a las URLs.

### Configurar Dominio Personalizado

1. En Render, ve a **Settings** → **Custom Domain**
2. Agrega tu dominio personalizado
3. Actualiza `ALLOWED_HOSTS` con el nuevo dominio

---

## 📝 Checklist Pre-Despliegue

- [x] Procfile creado
- [x] build.sh creado
- [x] requirements.txt actualizado con gunicorn y whitenoise
- [x] settings.py configurado para producción
- [x] Variables de entorno preparadas
- [ ] SECRET_KEY generada y segura
- [ ] ALLOWED_HOSTS configurado con dominio de Render
- [ ] Base de datos configurada
- [ ] Archivos estáticos configurados

---

## � Troubleshooting

### Error: "No module named 'gunicorn'"
- Verifica que `gunicorn` esté en `requirements.txt`
- Revisa los logs de construcción en Render

### Error: "DisallowedHost"
- Verifica que el dominio de Render esté en `ALLOWED_HOSTS`
- Revisa la variable de entorno `ALLOWED_HOSTS`

### Error: "Static files not found"
- Verifica que `collectstatic` se ejecute en el build
- Revisa la configuración de `STATIC_ROOT` y `STATICFILES_STORAGE`

### Error de conexión a base de datos
- Verifica las credenciales de la base de datos
- Asegúrate de que el host de la BD permita conexiones desde Render
- Verifica que el puerto sea correcto

---

## 🔗 URLs después del Despliegue

Una vez desplegado, tu aplicación estará disponible en:
- `https://tu-app.onrender.com`
- `https://tu-app.onrender.com/admin/` (panel de administración)

---

## 📚 Recursos Adicionales

- [Documentación de Render](https://render.com/docs)
- [Desplegar Django en Render](https://render.com/docs/deploy-django)
- [Configuración de Variables de Entorno](https://render.com/docs/environment-variables)

