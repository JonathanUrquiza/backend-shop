# Cómo Agregar el Dominio de Render Después de Crear el Servicio

## 📍 Situación

Has creado el servicio en Render pero aún no tienes el dominio asignado. Render asigna el dominio **después** de crear el servicio.

---

## 🔍 Paso 1: Encontrar tu Dominio de Render

### Opción A: En el Dashboard Principal
1. Ve a tu servicio en Render
2. En la parte superior de la página verás el dominio asignado
3. Se verá algo como: `https://tu-app-xxxx.onrender.com`

### Opción B: En Settings → Domains
1. Ve a tu servicio en Render
2. Haz clic en **Settings** (en el menú lateral)
3. Busca la sección **"Domains"**
4. Ahí verás el dominio asignado por Render

### Opción C: En los Logs
1. Ve a **Logs** de tu servicio
2. Busca mensajes que mencionen el dominio o URL

---

## ⚙️ Paso 2: Actualizar ALLOWED_HOSTS

Una vez que tengas el dominio (ejemplo: `ecommerce-shop-abc123.onrender.com`):

### Método 1: Desde el Dashboard de Render

1. Ve a tu servicio en Render
2. Haz clic en **Environment** (en el menú lateral izquierdo)
3. Busca la variable `ALLOWED_HOSTS`
4. Haz clic en el ícono de **editar** (lápiz) o en el valor actual
5. Actualiza el valor:
   ```
   ecommerce-shop-abc123.onrender.com,localhost,127.0.0.1
   ```
   **Nota:** Solo el nombre del dominio, SIN `https://` y SIN la barra final `/`
6. Haz clic en **Save Changes**
7. Render reiniciará automáticamente tu servicio

### Método 2: Agregar Nueva Variable (si no existe)

Si no tienes la variable `ALLOWED_HOSTS`:

1. Ve a **Environment**
2. Haz clic en **Add Environment Variable**
3. **Key:** `ALLOWED_HOSTS`
4. **Value:** `tu-dominio.onrender.com,localhost,127.0.0.1`
5. Haz clic en **Save Changes**

---

## ✅ Paso 3: Verificar que Funciona

1. Espera a que Render termine de reiniciar (verás "Live" en verde)
2. Abre tu navegador y ve a: `https://tu-dominio.onrender.com`
3. Deberías ver tu aplicación funcionando

Si ves un error de "DisallowedHost":
- Verifica que el dominio en `ALLOWED_HOSTS` sea exactamente igual al que Render te asignó
- Asegúrate de que no tenga `https://` ni `/` al final
- Verifica que hayas guardado los cambios

---

## 🔄 Si Cambias el Nombre del Servicio

Si cambias el nombre de tu servicio en Render, el dominio también cambiará:

1. El nuevo dominio será: `https://nuevo-nombre-xxxx.onrender.com`
2. Actualiza `ALLOWED_HOSTS` con el nuevo dominio
3. Render reiniciará automáticamente

---

## 🌐 Dominio Personalizado (Opcional)

Si quieres usar tu propio dominio:

1. Ve a **Settings** → **Custom Domain**
2. Agrega tu dominio personalizado (ej: `api.tudominio.com`)
3. Sigue las instrucciones de DNS que Render te proporciona
4. Actualiza `ALLOWED_HOSTS` para incluir también tu dominio personalizado:
   ```
   tu-dominio.onrender.com,api.tudominio.com,localhost,127.0.0.1
   ```

---

## 📝 Ejemplo Completo

**Dominio asignado por Render:**
```
https://ecommerce-shop-abc123.onrender.com
```

**Variable ALLOWED_HOSTS:**
```
ALLOWED_HOSTS=ecommerce-shop-abc123.onrender.com,localhost,127.0.0.1
```

**URLs de acceso:**
- API Base: `https://ecommerce-shop-abc123.onrender.com/`
- Admin: `https://ecommerce-shop-abc123.onrender.com/admin/`
- Productos: `https://ecommerce-shop-abc123.onrender.com/product/list/`

---

## ⚠️ Errores Comunes

### Error: "DisallowedHost at /"
**Solución:** Verifica que el dominio en `ALLOWED_HOSTS` coincida exactamente con el de Render (sin `https://`)

### Error: "Invalid HTTP_HOST header"
**Solución:** Asegúrate de que el dominio esté en `ALLOWED_HOSTS` y que hayas guardado los cambios

### El servicio no se reinicia después de cambiar variables
**Solución:** Render debería reiniciar automáticamente. Si no, haz clic en **Manual Deploy** → **Deploy latest commit**

---

## 💡 Tip

Puedes agregar múltiples dominios separados por comas:
```
ALLOWED_HOSTS=dominio1.onrender.com,dominio2.onrender.com,localhost,127.0.0.1
```

