# Guía de Debugging para Render

## 🔍 Cómo Obtener y Compartir los Logs

### Paso 1: Obtener los Logs de Render

1. Ve a tu servicio en Render
2. Haz clic en **"Logs"** en el menú lateral
3. Verás los logs en tiempo real
4. **Copia los últimos logs** (especialmente los errores)

### Paso 2: Identificar el Tipo de Error

Los errores comunes en Render son:

#### Error de Build (durante la construcción)
- Aparece durante el proceso de construcción
- Busca líneas que digan "ERROR" o "FAILED"

#### Error de Runtime (cuando la app está corriendo)
- Aparece después de que el build termina
- Busca errores de Python, Django, o conexión a BD

#### Error de Conexión a Base de Datos
- Busca mensajes como "OperationalError", "Connection refused", "Access denied"

---

## 🐛 Errores Comunes y Soluciones

### Error: "No module named 'gunicorn'"
**Solución:**
- Verifica que `gunicorn>=21.2.0` esté en `requirements.txt`
- Asegúrate de que el build command incluya `pip install -r requirements.txt`

### Error: "DisallowedHost"
**Solución:**
- Verifica que `ALLOWED_HOSTS` incluya tu dominio de Render
- Formato correcto: `tu-app.onrender.com,localhost,127.0.0.1`
- Sin `https://` y sin `/` al final

### Error: "ModuleNotFoundError: No module named 'X'"
**Solución:**
- Verifica que todas las dependencias estén en `requirements.txt`
- Revisa que el build command instale las dependencias

### Error: "OperationalError: (2003, 'Can't connect to MySQL server')"
**Solución:**
- Verifica las variables de entorno de la base de datos
- Asegúrate de que el host de MySQL permita conexiones externas
- Verifica que el puerto sea correcto (3306 para MySQL)

### Error: "collectstatic" falla
**Solución:**
- Verifica que `STATIC_ROOT` esté configurado en `settings.py`
- Asegúrate de que `whitenoise` esté en `requirements.txt` e `INSTALLED_APPS`

### Error: "SECRET_KEY not set"
**Solución:**
- Verifica que la variable de entorno `SECRET_KEY` esté configurada en Render
- Debe tener un valor válido

---

## 📋 Checklist de Verificación

Antes de pedir ayuda, verifica:

- [ ] `requirements.txt` incluye todas las dependencias
- [ ] `Procfile` tiene el comando correcto: `web: gunicorn Ecommerce.wsgi:application`
- [ ] Build command incluye `pip install -r requirements.txt`
- [ ] Variables de entorno están configuradas correctamente
- [ ] `ALLOWED_HOSTS` incluye el dominio de Render
- [ ] `DEBUG=False` en producción
- [ ] `SECRET_KEY` está configurada y es segura

---

## 🔧 Comandos Útiles para Debugging Local

### Probar el build localmente

```bash
# Instalar dependencias
pip install -r requirements.txt

# Recolectar archivos estáticos
python manage.py collectstatic --no-input

# Probar que gunicorn funciona
gunicorn Ecommerce.wsgi:application --check-config
```

### Verificar configuración

```bash
# Verificar settings
python manage.py check --deploy

# Verificar conexión a BD
python manage.py dbshell
```

---

## 📝 Formato para Compartir Errores

Cuando compartas los logs, incluye:

1. **Tipo de error:** Build o Runtime
2. **Mensaje completo del error** (últimas 20-30 líneas)
3. **Configuración actual:**
   - Build Command
   - Start Command
   - Variables de entorno (sin mostrar passwords)
4. **Archivos relevantes:**
   - `requirements.txt`
   - `Procfile`
   - `settings.py` (solo las partes relevantes)

---

## 💡 Tips para Debugging

1. **Revisa los logs completos:** A veces el error real está más arriba en los logs
2. **Verifica el build log primero:** Muchos errores ocurren durante el build
3. **Prueba localmente:** Si funciona localmente, el problema es de configuración en Render
4. **Revisa las variables de entorno:** Un typo puede causar errores

---

## 🆘 Si Necesitas Ayuda

Comparte conmigo:
1. Los logs de error completos
2. Tu configuración actual (Build Command, Start Command)
3. Las variables de entorno (sin passwords)
4. Cualquier cambio que hayas hecho recientemente

