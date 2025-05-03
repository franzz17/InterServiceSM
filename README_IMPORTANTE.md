# SOLUCIONES PARA PROBLEMAS COMUNES EN INTERSERVICESSM

## 1. SOLUCIÓN AL ERROR DE TABLAS EN DJANGO

Este es un problema común al trabajar con Django y bases de datos PostgreSQL existentes: las tablas del sistema de Django no existen en tu base de datos. Esto causa errores como:

```
django.db.utils.ProgrammingError: relation "django_session" does not exist
django.db.utils.ProgrammingError: relation "django_content_type" does not exist
```

### SOLUCIÓN RÁPIDA

Para resolver este problema, usa el script que he creado:

1. Abre una terminal en la carpeta del proyecto (`C:\Users\LENOVO\Desktop\Proyecto`)
2. Asegúrate de tener activado el entorno virtual:
   ```
   venv\Scripts\activate
   ```
3. Instala psycopg2 si aún no lo tienes:
   ```
   pip install psycopg2-binary
   ```
4. Ejecuta el script:
   ```
   python create_all_django_tables.py
   ```
5. Registra las migraciones en Django:
   ```
   python manage.py migrate --fake
   ```
6. Reinicia el servidor:
   ```
   python manage.py runserver
   ```

### ¿QUÉ HACE ESTE SCRIPT?

El script `create_all_django_tables.py` crea todas las tablas necesarias del sistema de Django:

- `django_session`: Para manejar sesiones (necesario para el login)
- `django_content_type`: Para el sistema de contenidos
- `auth_user`, `auth_permission`, etc.: Para el sistema de autenticación
- Otras tablas necesarias para el funcionamiento básico de Django

### ¿POR QUÉ OCURRE ESTE PROBLEMA?

Este problema ocurre porque:

1. Estás conectando Django a una base de datos PostgreSQL existente
2. Esta base de datos ya tiene tablas personalizadas (`solicitudes`, `clientes`)
3. Pero no tiene las tablas del sistema que Django necesita para funcionar

### DESPUÉS DE EJECUTAR EL SCRIPT

Una vez que el script se ejecute correctamente y registres las migraciones:

1. Podrás iniciar sesión en el panel de administración
2. Podrás ver y gestionar las solicitudes
3. Todo el sistema de flujo de trabajo funcionará correctamente

## 2. CONFIGURACIÓN DEL ENVÍO DE CORREOS

Para configurar el envío de correos electrónicos, sigue estos pasos:

1. **Actualiza las credenciales en settings.py**:
   ```python
   EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
   EMAIL_HOST = 'smtp.gmail.com'
   EMAIL_PORT = 587
   EMAIL_USE_TLS = True
   EMAIL_HOST_USER = 'tu_correo@gmail.com'
   EMAIL_HOST_PASSWORD = 'tu_contraseña_de_aplicacion'
   DEFAULT_FROM_EMAIL = 'InterServicesSM <tu_correo@gmail.com>'
   ```

2. **Creación de contraseña de aplicación para Gmail**:
   - Accede a tu cuenta de Google
   - Ve a "Seguridad" en tu cuenta
   - Activa la "Verificación en dos pasos" si no está activa
   - Ve a "Contraseñas de aplicaciones"
   - Selecciona "Aplicación: Otra (nombre personalizado)" y llama a la aplicación "InterServicesSM"
   - Copia la contraseña generada (16 caracteres) y úsala en `EMAIL_HOST_PASSWORD`

3. **Descomenta las líneas de envío de correos en views.py**:
   Busca las líneas comentadas `# send_mail(subject, message, from_email, recipient_list)` y descoméntalas.

## 3. PROBLEMAS COMUNES DE GOOGLE CLOUD STORAGE

Si tienes problemas al subir archivos a Google Cloud Storage:

1. **Verifica las credenciales**: Asegúrate de que el archivo `credentials.json` está en la raíz del proyecto

2. **Permisos del bucket**: Verifica que el bucket "interservicesm" existe y tiene los permisos adecuados

3. **Uniform bucket-level access**: Esta opción debe estar habilitada, por lo que no debemos usar ACLs a nivel de objeto

4. **Solución alternativa**: Si continuas con problemas, el sistema usará automáticamente almacenamiento local en la carpeta `media/`

## 4. ERRORES CON LA TABLA DE CLIENTES

Si recibes errores relacionados con la tabla `clientes` no encontrada:

1. Ejecuta el script `create_clientes_table.py`:
   ```
   python create_clientes_table.py
   ```

2. Alternativamente, la tabla se creará automáticamente la primera vez que se intente completar una solicitud

## 5. ERRORES DE SESIÓN

Si encuentras errores relacionados con sesiones expiradas o problemas de inicio de sesión:

1. Ejecuta el script `solve_session_error.py`:
   ```
   python solve_session_error.py
   ```

2. Si el problema persiste, borra todas las cookies del navegador e intenta nuevamente

Si tienes alguna duda o problema adicional, no dudes en informarlo.

