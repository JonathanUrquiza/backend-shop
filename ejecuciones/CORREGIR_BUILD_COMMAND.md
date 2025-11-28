# Cómo Corregir el Build Command en Render

## 🔴 Problema Actual

El Build Command en Render tiene este formato incorrecto:
```
`./build.sh` o `pip install -r requirements.txt && python manage.py collectstatic --no-input`
```

Esto causa errores porque Render está intentando ejecutar caracteres especiales como comandos.

---

## ✅ Solución: Corregir Build Command en Render

### Opción 1: Usar Comando Directo (Recomendado)

1. Ve a tu servicio en Render
2. Haz clic en **Settings** (en el menú lateral izquierdo)
3. Busca la sección **"Build & Deploy"**
4. Encuentra el campo **"Build Command"**
5. **Borra todo el contenido actual**
6. Escribe exactamente esto (sin comillas, sin acentos, sin caracteres especiales):
   ```
   pip install -r requirements.txt && python manage.py collectstatic --no-input
```


7. Haz clic en **Save Changes**
8. Render reiniciará automáticamente el despliegue

### Opción 2: Usar el Script build.sh

Si prefieres usar el script build.sh:

1. En **Build Command**, escribe:
   ```
   chmod +x build.sh && ./build.sh
   ```

---

## 📋 Configuración Completa Correcta

### Build Command:
```
pip install -r requirements.txt && python manage.py collectstatic --no-input
```

### Start Command:
```
gunicorn Ecommerce.wsgi:application
```

### Runtime:
- **Python Version**: 3.13.4 (o especifica 3.11 o 3.12 si hay problemas)

---

## ⚠️ Importante

- **NO uses comillas** en el Build Command
- **NO uses caracteres especiales** como ` o `
- **NO uses "o"** como separador de comandos
- Usa **solo** el comando directo o el script

---

## 🔍 Verificación

Después de cambiar el Build Command:

1. Render debería comenzar un nuevo build automáticamente
2. En los logs deberías ver:
   ```
   Installing dependencies...
   Collecting static files...
   Build completed successfully!
   ```

---

## 🐛 Si Sigue Fallando

Si después de corregir el Build Command sigue fallando:

1. Verifica que `requirements.txt` esté en la raíz del proyecto
2. Verifica que `manage.py` esté en la raíz del proyecto
3. Revisa los logs completos para ver el error específico
4. Asegúrate de que no haya espacios extra al inicio o final del Build Command

