# Configuración Completa para Render

## 🚀 Configuración del Servicio

### Build Command
```
pip install -r requirements.txt && python manage.py collectstatic --no-input
```

### Start Command
```
gunicorn Ecommerce.wsgi:application
```

### Runtime
- **Environment**: Python 3
- **Python Version**: 3.13.4 (o 3.11/3.12)

---

## 🔐 Variables de Entorno

### Variables Obligatorias

```
SECRET_KEY=tu-clave-secreta-generada
DEBUG=False
DB_NAME=funkotest_funkos
DB_USER=funkotest
DB_PASS=tu-password
DB_HOST=mysql-funkotest.alwaysdata.net
DB_PORT=3306
```

### Variable ALLOWED_HOSTS

**Configurar DESPUÉS de obtener el dominio de Render:**

```
ALLOWED_HOSTS=tu-app-xxxx.onrender.com,localhost,127.0.0.1
```

**Nota:** Reemplaza `tu-app-xxxx.onrender.com` con tu dominio real de Render.

---

## 📋 Checklist Rápido

- [ ] Build Command configurado (sin comillas)
- [ ] Start Command configurado
- [ ] Variables de entorno agregadas
- [ ] SECRET_KEY generada
- [ ] ALLOWED_HOSTS actualizado con dominio de Render

---

## 🔑 Generar SECRET_KEY

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

---

## 📁 Archivos Necesarios

- ✅ `Procfile` - Comando de inicio
- ✅ `requirements.txt` - Dependencias
- ✅ `manage.py` - Script Django
- ✅ `Ecommerce/wsgi.py` - WSGI config

---

## 🌐 URLs Post-Despliegue

- API: `https://tu-app.onrender.com/`
- Admin: `https://tu-app.onrender.com/admin/`
- Productos: `https://tu-app.onrender.com/product/list/`

---

## 📚 Documentación Completa

Ver `ejecuciones/CONFIGURACION_RENDER_COMPLETA.md` para detalles completos.

