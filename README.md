# InterServicesSM - Plataforma de Servicios de Internet

Este proyecto consiste en una plataforma web completa para una empresa proveedora de servicios de internet, que incluye una página principal, formularios de solicitud de servicio y revisión técnica, un portal de inicio de sesión para clientes y un panel de administración para gestionar las solicitudes y visualizar métricas.

## Características

- **Página Principal**: Muestra información sobre la empresa, misión, visión y servicios ofrecidos
- **Formulario de Solicitud**: Permite a los usuarios solicitar un nuevo servicio de internet
- **Formulario de Revisión Técnica**: Permite a los clientes solicitar una revisión de su servicio actual
- **Portal de Login**: Acceso para administradores para gestionar solicitudes
- **Panel de Administración**:
  - Vista de solicitudes pendientes, aprobadas y completadas
  - Asignación de instaladores y fechas de instalación
  - Visualización de documentos subidos
  - Flujo de trabajo para aprobar, rechazar o completar solicitudes
  - Envío de correos automáticos a clientes
- **Dashboard de Métricas**: Visualización de estadísticas sobre solicitudes e instalaciones
- **API REST**: Endpoint para consultar información de clientes por su número de cédula
- **Integración con PostgreSQL**: Almacenamiento de datos en base de datos PostgreSQL
- **Integración con Google Cloud Storage**: Almacenamiento de archivos en la nube

## Requisitos

- Python 3.8+
- Django 4.2+
- PostgreSQL
- Google Cloud Storage (opcional, para producción)

## Configuración del Entorno

1. **Clonar el repositorio o descargar los archivos**

2. **Crear un entorno virtual**:
   ```bash
   python -m venv venv
   ```

3. **Activar el entorno virtual**:
   - En Windows:
     ```
     venv\Scripts\activate
     ```
   - En macOS/Linux:
     ```
     source venv/bin/activate
     ```

4. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Configurar el archivo de variables de entorno**:
   - Copia `.env.template` a `.env` y ajusta las variables según tu entorno

6. **Crear las tablas necesarias**:
   Puedes ejecutar el script SQL incluido:
   ```bash
   psql -h confidently-nifty-skylark.data-1.use1.tembo.io -U postgres -d postgres -f create_tables.sql
   ```
   O aplicar las migraciones:
   ```bash
   python manage.py migrate --fake
   ```
   (Usamos --fake porque algunas tablas ya pueden existir en PostgreSQL)

## Ejecución del Proyecto

Para iniciar el servidor de desarrollo:
```bash
python manage.py runserver
```

La aplicación estará disponible en:
- **Página Principal**: http://127.0.0.1:8000/
- **Formulario de Solicitud**: http://127.0.0.1:8000/formulario/
- **Formulario de Revisión**: http://127.0.0.1:8000/solicitud-revision/
- **Portal de Login**: http://127.0.0.1:8000/login/
- **Panel de Administración**: http://127.0.0.1:8000/admin-panel/ (tras iniciar sesión)
- **Dashboard de Métricas**: http://127.0.0.1:8000/dashboard/ (tras iniciar sesión)
- **Panel de Django Admin**: http://127.0.0.1:8000/admin/ (requiere crear superusuario)
- **API de Clientes**: http://127.0.0.1:8000/api/cliente/CEDULA/ (reemplazar CEDULA con número real)

## Credenciales de Administrador

Para acceder al panel de administración:
- **Usuario**: default
- **Contraseña**: default

## Flujo de Trabajo

1. **Solicitud de Servicio**:
   - Los usuarios completan el formulario de solicitud
   - Suben foto de cédula y recibo de servicio público
   - La solicitud se guarda con estado "Pendiente"

2. **Gestión de Solicitudes Pendientes**:
   - El administrador revisa las solicitudes pendientes
   - Verifica las imágenes subidas
   - Asigna un instalador y una fecha de instalación
   - Aprueba o rechaza la solicitud
   - Se envía un correo al cliente informando de la decisión

3. **Gestión de Solicitudes Aprobadas**:
   - El administrador puede ver las solicitudes aprobadas
   - Después de la instalación, marca la solicitud como completada
   - Opcionalmente agrega notas sobre la instalación
   - Se envía un correo de contrato al cliente
   - Los datos se transfieren a la tabla de clientes y se eliminan de solicitudes

4. **Gestión de Clientes**:
   - Los clientes con instalaciones completadas se pueden ver en la sección correspondiente
   - Se mantiene un registro permanente de todos los clientes activos
   - Se puede consultar información básica a través del API REST

5. **Solicitud de Revisión Técnica**:
   - Los clientes pueden solicitar una revisión de su servicio
   - Se verifica automáticamente si el cliente existe en la base de datos
   - Se envía un correo al técnico encargado con los detalles de la solicitud

6. **Análisis de Métricas**:
   - El administrador puede acceder al dashboard de métricas
   - Visualización de estadísticas sobre solicitudes pendientes, aprobadas y completadas
   - Análisis de distribución por planes y barrios
   - Seguimiento de tendencias mensuales

## API REST

El proyecto incluye un endpoint de API que permite consultar datos básicos de un cliente por su número de cédula:

- **URL**: `/api/cliente/<cedula>/`
- **Método**: GET
- **Ejemplo de respuesta** (cliente existente):
  ```json
  {
    "nombre": "Juan",
    "apellido": "Pérez",
    "plan_contratado": "Internet 100MB",
    "fecha_instalacion": "15/04/2025"
  }
  ```
- **Ejemplo de respuesta** (cliente no encontrado):
  ```json
  {
    "error": "Cliente no encontrado"
  }
  ```

## Google Cloud Storage

Para habilitar el almacenamiento de archivos en Google Cloud Storage:

1. Crea un bucket en Google Cloud Storage llamado "interservicesm"
2. Habilita el acceso uniforme a nivel de bucket
3. Configura el bucket para acceso público si es necesario
4. Coloca el archivo de credenciales (`credentials.json`) en la raíz del proyecto
5. Asegúrate de que las credenciales tienen los permisos necesarios para el bucket
6. Las configuraciones de GCS ya están habilitadas en `settings.py`

## Envío de Correos

Para configurar el envío real de correos:

1. Asegúrate de editar `settings.py` con tus credenciales de correo:
   ```python
   EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
   EMAIL_HOST = 'smtp.gmail.com'
   EMAIL_PORT = 587
   EMAIL_USE_TLS = True
   EMAIL_HOST_USER = 'tu_correo@gmail.com'
   EMAIL_HOST_PASSWORD = 'tu_contraseña_de_aplicacion' 
   DEFAULT_FROM_EMAIL = 'InterServicesSM <tu_correo@gmail.com>'
   ```
2. Para Gmail, debes crear una "contraseña de aplicación":
   - Accede a tu cuenta de Google > Seguridad
   - Activa la verificación en dos pasos
   - Ve a "Contraseñas de aplicaciones"
   - Crea una nueva contraseña para la aplicación
   - Copia la contraseña generada y pégala en EMAIL_HOST_PASSWORD

3. Asegúrate de que las líneas `send_mail()` estén descomentadas en el archivo `views.py`

Los correos se envían en los siguientes eventos:

- Cuando se aprueba una solicitud de servicio
- Cuando se rechaza una solicitud de servicio
- Cuando se completa una instalación
- Cuando hay un problema con las imágenes subidas
- Cuando se recibe una solicitud de revisión técnica

## Dashboard de Métricas

El dashboard de métricas proporciona las siguientes visualizaciones:

- **Estadísticas Generales**: Conteo de solicitudes pendientes, aprobadas y completadas
- **Distribución por Estado**: Gráfico circular con la proporción de solicitudes en cada estado
- **Distribución por Planes**: Gráfico de barras comparando los planes contratados
- **Tendencias Mensuales**: Gráfico de líneas mostrando solicitudes e instalaciones por mes
- **Distribución por Barrios**: Gráfico de barras con los barrios más populares
- **Tabla de Planes**: Resumen detallado de planes contratados

El dashboard utiliza Chart.js para las visualizaciones y se actualiza en tiempo real con datos de la base de datos.

## Estructura del Proyecto

- **proyecto/**: Configuración principal de Django
- **mi_app/**: Aplicación principal
  - **templates/mi_app/**: Plantillas HTML
    - **index.html**: Página principal
    - **formulario.html**: Formulario de solicitud
    - **solicitud_revision.html**: Formulario de revisión técnica
    - **login.html**: Portal de inicio de sesión
    - **admin_panel.html**: Panel de administración
    - **dashboard.html**: Dashboard de métricas
  - **models.py**: Modelos de datos (Solicitud, Cliente, Formulario)
  - **views.py**: Lógica de vistas y API
  - **storage_utils.py**: Utilidades para almacenamiento de archivos
  - **admin.py**: Configuración del admin de Django

## Solución de Problemas

- **Error al subir archivos**: Verifica que las carpetas media/Cedulas y media/Factura_sp existan y tengan permisos de escritura
- **Error de conexión a PostgreSQL**: Comprueba las credenciales en settings.py
- **Problemas con Google Cloud Storage**: Asegúrate de que el archivo credentials.json está presente y es válido
- **Error de tablas faltantes**: Ejecuta el script `create_all_django_tables.py` para crear las tablas del sistema de Django
- **Problemas con Chart.js**: Verifica la conexión a internet para cargar la biblioteca desde CDN

## Notas para Desarrollo

- En entorno de desarrollo, los archivos se guardan localmente si no se configura GCS
- La autenticación del admin es simple (usuario/contraseña fijos) para facilitar las pruebas
- El dashboard y el formulario de revisión técnica usan el API REST para consultar datos de clientes
