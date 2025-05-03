# DOCUMENTACIÓN DEL PROYECTO INTERSERVICESSM

## 1. INTRODUCCIÓN

### 1.1 Descripción General

InterServicesSM es una plataforma web integral diseñada para una empresa proveedora de servicios de internet. El sistema permite gestionar todo el proceso de solicitud de servicios, desde la petición inicial hasta la instalación y mantenimiento, ofreciendo a la vez herramientas de administración y análisis para el personal de la empresa.

### 1.2 Propósito del Sistema

El propósito principal del sistema es automatizar y facilitar los siguientes procesos:
- Recepción de solicitudes de nuevos servicios
- Gestión de las aprobaciones e instalaciones
- Mantenimiento de una base de datos de clientes
- Recepción y procesamiento de solicitudes de revisión técnica
- Análisis estadístico de los datos para la toma de decisiones

### 1.3 Alcance

El sistema cubre el ciclo completo de atención al cliente, desde la página informativa hasta la gestión post-venta:
- Presentación de información de la empresa y servicios
- Formularios para nuevas solicitudes y revisiones técnicas
- Panel de administración para gestionar solicitudes
- Dashboard para análisis de datos y métricas
- API REST para consulta de información de clientes
- Sistema de notificaciones por correo electrónico

## 2. ARQUITECTURA DEL SISTEMA

### 2.1 Tecnologías Utilizadas

- **Backend**: Django 4.2+ (Framework de Python)
- **Frontend**: HTML, CSS, JavaScript, Chart.js
- **Base de Datos**: PostgreSQL
- **Almacenamiento de Archivos**: Sistema de archivos local / Google Cloud Storage
- **Envío de Correos**: SMTP (Gmail)
- **Visualización de Datos**: Chart.js

### 2.2 Estructura del Proyecto

```
Proyecto/
│
├── mi_app/                          # Aplicación principal
│   ├── templates/                   # Plantillas HTML
│   │   └── mi_app/
│   │       ├── admin_panel.html     # Panel de administración
│   │       ├── dashboard.html       # Dashboard de métricas
│   │       ├── formulario.html      # Formulario de solicitud
│   │       ├── index.html           # Página principal
│   │       ├── login.html           # Página de login
│   │       └── solicitud_revision.html # Formulario de revisión técnica
│   │
│   ├── __init__.py
│   ├── admin.py                     # Configuración admin de Django
│   ├── apps.py
│   ├── models.py                    # Modelos de datos (Solicitud, Cliente)
│   ├── storage_utils.py             # Utilidades para almacenamiento en GCS
│   ├── tests.py
│   └── views.py                     # Vistas y lógica de negocio + API
│
├── proyecto/                        # Configuración del proyecto
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py                  # Configuración general
│   ├── urls.py                      # Definición de URLs
│   └── wsgi.py
│
├── media/                           # Archivos de media (desarrollo)
│   ├── Cedulas/                     # Imágenes de cédulas
│   └── Factura_sp/                  # Imágenes de recibos
│
├── credentials.json                 # Credenciales de Google Cloud
├── create_all_django_tables.py      # Script para crear tablas de Django
├── create_clientes_table.py         # Script para crear tabla clientes
├── create_tables.sql                # SQL para crear tablas en PostgreSQL
├── manage.py                        # Script de gestión de Django
└── requirements.txt                 # Dependencias del proyecto
```

### 2.3 Modelo de Datos

#### 2.3.1 Modelo Solicitud
```python
class Solicitud(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    cedula = models.CharField(max_length=20, unique=True)
    telefono = models.CharField(max_length=20)
    correo = models.EmailField()
    barrio = models.CharField(max_length=100)
    direccion = models.CharField(max_length=255)
    plan_seleccionado = models.CharField(max_length=50)
    preferencia_horario = models.CharField(max_length=50)
    url_cedula = models.URLField(max_length=500)
    url_recibo = models.URLField(max_length=500)
    instalador = models.CharField(max_length=100, null=True, blank=True)
    fecha_instalacion = models.DateTimeField(null=True, blank=True)
    estado = models.CharField(max_length=20, default='Pendiente')
    fecha_registro = models.DateTimeField(auto_now_add=True)
```

#### 2.3.2 Modelo Cliente
```python
class Cliente(models.Model):
    id_cliente = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    cedula = models.CharField(max_length=20, unique=True)
    telefono = models.CharField(max_length=20)
    correo = models.EmailField()
    barrio = models.CharField(max_length=100)
    direccion = models.CharField(max_length=255)
    plan_seleccionado = models.CharField(max_length=50)
    preferencia_horario = models.CharField(max_length=50)
    url_cedula = models.URLField(max_length=500)
    url_recibo = models.URLField(max_length=500)
    fecha_registro = models.DateTimeField(auto_now_add=True)
```

## 3. FUNCIONALIDADES DEL SISTEMA

### 3.1 Página Principal

La página principal (`index.html`) proporciona información sobre la empresa, sus servicios y ofrece enlaces a las diferentes funcionalidades del sistema. Incluye:

- Información sobre la empresa (misión, visión, valores)
- Descripción de los planes de internet ofrecidos
- Llamados a la acción (solicitar servicio, solicitar revisión, área de clientes)
- Información de contacto
- Menú de navegación

### 3.2 Formulario de Solicitud de Servicio

El formulario de solicitud (`formulario.html`) permite a los usuarios solicitar un nuevo servicio de internet. Características:

- Campos para información personal (nombre, apellido, cédula, etc.)
- Campos para dirección y ubicación
- Selección de plan de internet
- Selección de horario preferido para instalación
- Carga de documentos (cédula y recibo de servicio público)
- Validación de campos en cliente y servidor
- Mensajes de confirmación

### 3.3 Formulario de Solicitud de Revisión Técnica

El formulario de revisión técnica (`solicitud_revision.html`) permite a los clientes solicitar asistencia técnica para su servicio existente:

- Campos para información personal (nombre, apellido, cédula)
- Campo para descripción detallada del problema
- Auto-completado de información del cliente al ingresar cédula
- Validación de campos en cliente y servidor
- Verificación automática de existencia del cliente en la base de datos
- Envío de notificación por correo al técnico encargado
- Mensajes de confirmación y errores

### 3.4 Panel de Administración

El panel de administración (`admin_panel.html`) permite gestionar las solicitudes de servicio. Incluye:

- Vista de solicitudes pendientes
- Vista de solicitudes aprobadas
- Vista de clientes con instalaciones completadas
- Funciones para:
  - Aprobar solicitudes (asignar instalador y fecha)
  - Rechazar solicitudes (con motivo)
  - Completar instalaciones (trasladar a clientes)
  - Ver detalles completos de cada solicitud
- Validación de imágenes subidas por los clientes
- Interfaz intuitiva con modales para acciones
- Sistema de paginación para gestionar grandes volúmenes de solicitudes
- Enlace al dashboard de métricas

### 3.5 Dashboard de Métricas

El dashboard de métricas (`dashboard.html`) proporciona visualizaciones y estadísticas sobre las solicitudes e instalaciones:

- Resumen de estadísticas principales:
  - Contador de solicitudes pendientes
  - Contador de solicitudes aprobadas
  - Contador de instalaciones completadas
  - Total de solicitudes procesadas
- Visualizaciones gráficas:
  - Gráfico circular de distribución por estado (pendiente, aprobada, completada)
  - Gráfico de barras de distribución por planes contratados
  - Gráfico de líneas de tendencias mensuales
  - Gráfico de barras de distribución por barrios
- Tabla de resumen de planes contratados:
  - Planes activos vs. completados
  - Totales por plan
  - Porcentajes de distribución
- Integración con Chart.js para gráficos interactivos
- Diseño responsivo para visualización en diferentes dispositivos
- Actualización automática de datos al acceder a la página

### 3.6 API REST

El sistema incluye un endpoint de API RESTful para consultas de información de clientes:

- **Endpoint**: `/api/cliente/<cedula>/`
- **Método**: GET
- **Función**: Buscar datos de un cliente por número de cédula
- **Proceso**:
  - Valida el formato de la cédula (solo números)
  - Busca primero en la tabla de clientes (instalaciones completadas)
  - Retorna información en formato JSON
- **Respuesta exitosa**:
  ```json
  {
    "nombre": "Juan",
    "apellido": "Pérez",
    "plan_contratado": "Internet 100MB",
    "fecha_instalacion": "15/04/2025"
  }
  ```
- **Respuesta de error**:
  ```json
  {
    "error": "Cliente no encontrado"
  }
  ```
- Además de la API externa, el endpoint es utilizado internamente por:
  - El formulario de solicitud de revisión (para autocompletar datos)
  - El dashboard de métricas (para consultas estadísticas)

El sistema incluye un endpoint de API RESTful para consultas de información de posibles clientes:

- **Endpoint**: `/api/aprobadas/<cedula>/`
- **Método**: GET
- **Función**: Buscar datos de un posible cliente por número de cédula
- **Proceso**:
  - Valida el formato de la cédula (solo números)
  - Busca primero en la tabla de clientes (instalaciones completadas)
  - Retorna información en formato JSON
- **Respuesta exitosa**:
  ```json
  {
    "nombre": "Juan",
    "apellido": "Pérez",
    "plan_contratado": "Internet 100MB",
    "fecha_instalacion": "15/04/2025",
    "nota": "La instalacion aun no ha sido completada"
  }
  ```
- **Respuesta de error**:
  ```json
  {
    "error": "Posible cliente no encontrado"
  }
  ```

## 4. FLUJOS DE TRABAJO

### 4.1 Flujo de Solicitud de Nuevo Servicio

1. **Envío de solicitud**:
   - El usuario accede al formulario de solicitud desde la página principal
   - Completa sus datos personales y selecciona un plan y horario preferido
   - Sube imágenes de su cédula y recibo de servicio público
   - Envía el formulario, que es validado por el sistema
   - Se guarda la solicitud en la base de datos con estado "Pendiente"
   - Se muestra un mensaje de confirmación al usuario

2. **Revisión por administrador**:
   - El administrador accede al panel de administración
   - Visualiza las solicitudes pendientes
   - Revisa los detalles de cada solicitud, incluyendo las imágenes

3. **Aprobación de solicitud**:
   - Si todo está correcto, el administrador asigna un instalador y fecha
   - Marca la solicitud como "Aprobada" en el sistema
   - El sistema envía automáticamente un correo al cliente con los detalles de la instalación
   - La solicitud se mueve a la sección de "Solicitudes Aprobadas"

4. **Rechazo de solicitud**:
   - Si hay problemas, el administrador puede rechazar la solicitud
   - Debe proporcionar un motivo de rechazo
   - El sistema envía un correo al cliente informando del rechazo
   - La solicitud se elimina de la base de datos

5. **Completar instalación**:
   - Después de realizada la instalación, el administrador marca la solicitud como completada
   - Puede añadir notas opcionales sobre la instalación
   - El sistema transfiere los datos del cliente a la tabla de clientes
   - Se envía un correo de contrato al cliente
   - La solicitud se elimina de la tabla de solicitudes
   - El cliente aparece ahora en la sección de "Instalaciones Completadas"

### 4.2 Flujo de Solicitud de Revisión Técnica

1. **Envío de solicitud de revisión**:
   - El cliente accede al formulario de revisión desde la página principal
   - Ingresa su número de cédula
   - El sistema verifica si el cliente existe y autocompleta sus datos
   - El cliente describe el problema que está experimentando
   - Envía el formulario, que es validado por el sistema

2. **Notificación al técnico**:
   - El sistema envía automáticamente un correo al técnico encargado (fredisjuve@gmail.com)
   - El correo incluye todos los datos del cliente y la descripción del problema
   - Si el cliente no está registrado en la base de datos, se incluye una nota especial en el correo
   - Se muestra un mensaje de confirmación al cliente

### 4.3 Flujo de Análisis de Métricas

1. **Acceso al dashboard**:
   - El administrador inicia sesión en el sistema
   - Accede al dashboard desde el menú de navegación

2. **Visualización de métricas**:
   - El sistema recopila y procesa datos estadísticos de la base de datos
   - Muestra los contadores de resumen con cifras clave
   - Genera los gráficos visuales (distribución por estado, planes, barrios, etc.)
   - Muestra la tabla de resumen de planes contratados

3. **Análisis de datos**:
   - El administrador puede analizar tendencias y patrones
   - La información ayuda en la toma de decisiones estratégicas
   - Se pueden identificar áreas de mejora o oportunidades de negocio

## 5. TECNOLOGÍAS Y CONFIGURACIONES

### 5.1 Base de Datos PostgreSQL

El sistema utiliza PostgreSQL como gestor de base de datos relacional:

- **Host**: confidently-nifty-skylark.data-1.use1.tembo.io
- **Nombre BD**: postgres
- **Usuario**: postgres
- **Contraseña**: n5rNZneopwuKZiDd
- **Tablas principales**:
  - `solicitudes`: Almacena solicitudes pendientes y aprobadas
  - `clientes`: Almacena clientes con instalaciones completadas

**Notas sobre la base de datos**:
- Las tablas fueron creadas manualmente y luego conectadas a Django
- Es necesario ejecutar scripts auxiliares para crear tablas de sistema
- Se incluyen mecanismos para crear tablas automáticamente si no existen

### 5.2 Almacenamiento de Archivos

El sistema puede utilizar dos métodos para almacenar archivos:

1. **Desarrollo local**:
   - Archivos guardados en el sistema de archivos local
   - Estructura de carpetas: `media/Cedulas/` y `media/Factura_sp/`
   - URLs generadas con rutas relativas

2. **Producción (Google Cloud Storage)**:
   - Archivos almacenados en bucket "interservicesm"
   - Se requiere archivo de credenciales `credentials.json`
   - Estructura de carpetas en GCS: "Cedulas/" y "Factura_sp/"
   - URLs generadas con rutas públicas a GCS

**Configuración en settings.py**:
```python
DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
GS_BUCKET_NAME = 'interservicesm'
GS_PROJECT_ID = 'tu_id_proyecto'
GS_CREDENTIALS = os.path.join(BASE_DIR, 'credentials.json')
GS_QUERYSTRING_AUTH = False
```

### 5.3 Sistema de Correos Electrónicos

El sistema utiliza el módulo de correo de Django con SMTP para enviar notificaciones:

**Configuración en settings.py**:
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'dev.rpa.fredisbobadillo@gmail.com'
EMAIL_HOST_PASSWORD = 'apxz ezhx dytm ezvw'
DEFAULT_FROM_EMAIL = 'InterServicesSM <dev.rpa.fredisbobadillo@gmail.com>'
```

**Eventos que generan correos**:
- Aprobación de solicitud (al cliente)
- Rechazo de solicitud (al cliente)
- Instalación completada (al cliente)
- Problemas con imágenes subidas (al cliente)
- Solicitud de revisión técnica (al técnico)

### 5.4 Visualizaciones con Chart.js

El dashboard utiliza Chart.js para las visualizaciones gráficas:

- Cargado desde CDN: `<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>`
- Tipos de gráficos utilizados:
  - Gráfico circular (doughnut): Para distribución por estado
  - Gráfico de barras: Para distribución por planes y barrios
  - Gráfico de líneas: Para tendencias mensuales
- Datos generados dinámicamente desde consultas SQL
- Formato JSON para pasar datos desde backend a frontend

### 5.5 Autenticación y Seguridad

El sistema utiliza un mecanismo simple de autenticación:

- Credenciales fijas para administradores:
  - Usuario: `default`
  - Contraseña: `default`
- Sesiones de Django para mantener el estado de login
- Decorador personalizado `@admin_required` para proteger vistas
- CSRF habilitado en todos los formularios
- Validación de datos tanto en cliente como en servidor
- Validación especial para cédulas (solo números)

## 6. INSTALACIÓN Y DESPLIEGUE

### 6.1 Requisitos del Sistema

- Python 3.8+
- Django 4.2+
- Dependencias listadas en `requirements.txt`
- PostgreSQL
- Acceso SMTP para envío de correos
- (Opcional) Cuenta de Google Cloud para almacenamiento

### 6.2 Instalación en Entorno de Desarrollo

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

5. **Configuración de la base de datos**:
   - Configurar conexión a PostgreSQL en `settings.py`
   - Ejecutar script para crear tablas:
     ```bash
     python create_all_django_tables.py
     python manage.py migrate --fake
     ```

6. **Configuración de archivos estáticos y media**:
   - Crear carpetas necesarias:
     ```bash
     mkdir -p media/Cedulas media/Factura_sp
     ```

7. **Iniciar servidor de desarrollo**:
   ```bash
   python manage.py runserver
   ```

### 6.3 Despliegue en Producción

Para un entorno de producción, se recomienda:

1. **Configurar variables de entorno**:
   - Mover credenciales sensibles a variables de entorno
   - Actualizar `settings.py` para usar variables de entorno

2. **Configurar Google Cloud Storage**:
   - Crear bucket en GCS
   - Habilitar acceso uniforme a nivel de bucket
   - Generar archivo de credenciales y colocarlo en el proyecto
   - Verificar configuración en `settings.py`

3. **Configurar servidor web**:
   - Usar Gunicorn o uWSGI como servidor WSGI
   - Configurar Nginx como proxy inverso
   - Habilitar HTTPS con certificados SSL

4. **Configurar base de datos**:
   - Usar conexión segura a PostgreSQL
   - Habilitar backups automáticos

5. **Otras consideraciones**:
   - Habilitar registro de logs
   - Configurar monitoreo
   - Implementar estrategia de despliegue continuo

## 7. MANTENIMIENTO Y SOLUCIÓN DE PROBLEMAS

### 7.1 Problemas Comunes y Soluciones

1. **Error al crear tablas de Django**:
   - Ejecutar `python create_all_django_tables.py`
   - Seguido de `python manage.py migrate --fake`

2. **Error al visualizar clientes completados**:
   - Verificar existencia de tabla `clientes`
   - Ejecutar `python create_clientes_table.py` si es necesario

3. **Error al subir archivos**:
   - Verificar permisos en carpetas `media/`
   - Comprobar configuración de Google Cloud Storage

4. **Error en envío de correos**:
   - Verificar configuración SMTP en `settings.py`
   - Asegurarse de que las líneas `send_mail()` no estén comentadas
   - Revisar filtros de spam en cuenta de correo

5. **Error en el dashboard de métricas**:
   - Verificar conexión a Internet (Chart.js se carga desde CDN)
   - Revisar consola del navegador para errores JavaScript
   - Validar que las consultas SQL estén devolviendo datos correctos

### 7.2 Actualizaciones y Mejoras

Para futuras actualizaciones y mejoras, considerar:

1. **Sistema de usuarios completo**:
   - Implementar sistema de usuarios de Django
   - Roles y permisos (admin, técnico, cliente)
   - Recuperación de contraseñas

2. **Mejoras en el dashboard**:
   - Gráficos más avanzados
   - Filtros de fechas
   - Exportación de datos

3. **Seguimiento de revisiones técnicas**:
   - Tabla para almacenar historial de revisiones
   - Panel para técnicos
   - Estados y resolución de problemas

4. **Integración con sistemas externos**:
   - Pasarelas de pago
   - SMS para notificaciones
   - Mapas para ubicaciones

5. **Optimizaciones**:
   - Caché para consultas frecuentes
   - Mejoras de rendimiento en consultas SQL
   - Proceso de subida de archivos más eficiente

## 8. CONCLUSIONES

InterServicesSM es una plataforma completa que aborda todas las necesidades de gestión de una empresa proveedora de servicios de internet. Sus principales fortalezas son:

1. **Proceso integral**: Manejo del ciclo completo desde solicitud hasta post-venta
2. **Panel administrativo eficiente**: Herramientas para gestión rápida de solicitudes
3. **Métricas visuales**: Dashboard para análisis de datos y toma de decisiones
4. **API flexible**: Acceso a datos de clientes para integraciones
5. **Comunicación automática**: Sistema de notificaciones por correo electrónico

El sistema está diseñado para ser escalable y adaptable a las necesidades cambiantes de la empresa. Las oportunidades de mejora se centran en expandir las funcionalidades existentes y agregar nuevas capacidades para mejorar la experiencia tanto de los administradores como de los clientes.

---

## ANEXOS

### A1. Diagrama de Flujo del Sistema

```
+------------------------+     +------------------------+     +------------------------+
|                        |     |                        |     |                        |
|    Página Principal    +---->|  Formulario Solicitud  +---->| Solicitud en Base de  |
|                        |     |                        |     |        Datos           |
+------------------------+     +------------------------+     +----------+-------------+
                                                                         |
                                                                         v
+------------------------+     +------------------------+     +------------------------+
|                        |     |                        |     |                        |
|  Cliente Convertido    |<----+  Instalación Completa  |<----+  Aprobación Admin     |
|                        |     |                        |     |                        |
+------------------------+     +------------------------+     +------------------------+
        |
        |                       +------------------------+
        |                       |                        |
        +---------------------->|  Solicitud Revisión    |
                                |                        |
                                +----------+-------------+
                                           |
                                           v
                                +------------------------+
                                |                        |
                                |  Notificación Técnico  |
                                |                        |
                                +------------------------+
```

### A2. Referencias

- Django Documentation: https://docs.djangoproject.com/
- PostgreSQL Documentation: https://www.postgresql.org/docs/
- Chart.js Documentation: https://www.chartjs.org/docs/
- Google Cloud Storage: https://cloud.google.com/storage/docs
