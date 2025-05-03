# README PARA CONTEXTO DE IA - PROYECTO INTERSERVICESSM

Este documento proporciona un resumen completo del proyecto para que la IA pueda contextualizarse rápidamente en caso de alcanzar límites de longitud de conversación.

## ESTRUCTURA DEL PROYECTO

```
Proyecto/
│
├── mi_app/                          # Aplicación principal
│   ├── templates/                   # Plantillas HTML
│   │   └── mi_app/
│   │       ├── admin_panel.html     # Panel de administración
│   │       ├── formulario.html      # Formulario de solicitud
│   │       ├── index.html           # Página principal
│   │       └── login.html           # Página de login
│   │
│   ├── __init__.py
│   ├── admin.py                     # Configuración admin de Django
│   ├── apps.py
│   ├── models.py                    # Modelos de datos (Solicitud, Cliente)
│   ├── storage_utils.py             # Utilidades para almacenamiento en GCS
│   ├── tests.py
│   └── views.py                     # Vistas y lógica de negocio
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
├── credentials.json                 # Credenciales de Google Cloud (no en repo)
├── create_all_django_tables.py      # Script para crear tablas de Django
├── create_clientes_table.py         # Script para crear tabla clientes
├── create_tables.sql                # SQL para crear tablas en PostgreSQL
├── db.sqlite3                       # Base de datos local (no usada)
├── manage.py                        # Script de gestión de Django
├── requirements.txt                 # Dependencias del proyecto
└── README.md                        # Documentación general
```

## DESCRIPCIÓN GENERAL

InterServicesSM es una plataforma web para una empresa proveedora de servicios de internet que permite:

1. **Página Principal**: Muestra información sobre la empresa, misión, visión y servicios
2. **Formulario de Solicitud**: Permite a usuarios solicitar un nuevo servicio
3. **Panel de Administración**: Para gestionar solicitudes (pendientes, aprobadas, completadas)
4. **Sistema de Email**: Notifica a clientes sobre cambios en sus solicitudes

## MODELOS DE DATOS

### 1. Solicitud
- Almacena solicitudes de servicio pendientes o aprobadas
- Tabla en PostgreSQL: `solicitudes`
- Campos principales: nombre, apellido, cedula, telefono, correo, barrio, direccion, plan_seleccionado, preferencia_horario, url_cedula, url_recibo, instalador, fecha_instalacion, estado

### 2. Cliente
- Almacena clientes con instalaciones completadas
- Tabla en PostgreSQL: `clientes`
- Campos similares a Solicitud, pero sin instalador, fecha_instalacion o estado

## FLUJO DE TRABAJO

1. **Solicitud de Servicio**:
   - Usuario completa formulario con datos personales
   - Sube cédula y recibo de servicio público
   - Solicitud se guarda en tabla `solicitudes` con estado "Pendiente"

2. **Aprobación**:
   - Admin revisa solicitudes pendientes
   - Asigna instalador y fecha de instalación
   - Se envía correo al cliente con detalles
   - Estado cambia a "Aprobada"

3. **Completar Instalación**:
   - Admin marca la solicitud como completada
   - Datos se transfieren a tabla `clientes`
   - Se envía correo de contrato al cliente
   - Solicitud se elimina de tabla `solicitudes`

4. **Rechazo**:
   - Admin puede rechazar solicitudes
   - Se notifica al cliente por correo
   - Solicitud se elimina de tabla `solicitudes`

## AUTENTICACIÓN

- Sistema simple con credenciales fijas
- Usuario: `default`
- Contraseña: `default`
- Se utiliza la sesión de Django para mantener el estado de login

## ALMACENAMIENTO DE ARCHIVOS

- Desarrollo: Archivos guardados localmente en carpetas media/
- Producción: Google Cloud Storage en bucket "interservicesm"
- Estructura de carpetas en GCS: "Cedulas/" y "Factura_sp/"

## SISTEMA DE CORREOS

- Se utiliza Gmail como proveedor de correo electrónico
- Configuración SMTP activada en settings.py con:
  ```python
  EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
  EMAIL_HOST = 'smtp.gmail.com'
  EMAIL_PORT = 587
  EMAIL_USE_TLS = True
  EMAIL_HOST_USER = 'correo@gmail.com'
  EMAIL_HOST_PASSWORD = 'contraseña_de_aplicacion'
  DEFAULT_FROM_EMAIL = 'InterServicesSM <correo@gmail.com>'
  ```
- Se envían correos automáticos para notificar al cliente cuando:
  - Su solicitud es aprobada (con detalles de la instalación)
  - Su solicitud es rechazada (con el motivo)
  - Su instalación es completada (con el contrato de servicio)
  - Hay problemas con las imágenes subidas

## PROBLEMAS CONOCIDOS Y SOLUCIONES

### 1. Tablas de Django faltantes
- Problema: PostgreSQL existente no tiene tablas de sistema de Django
- Solución: Script create_all_django_tables.py que crea todas las tablas necesarias

### 2. Problema con tabla clientes
- Problema: Tabla clientes puede no existir al acceder a vista de clientes completados
- Solución: Script create_clientes_table.py y código que crea tabla automáticamente cuando se necesita

### 3. Problemas con Google Cloud Storage
- Problema: Error al subir archivos si no hay credenciales o ACLs inválidos
- Solución: Configuración correcta en settings.py y manejo graceful con almacenamiento local fallback

### 4. Problemas con el envío de correos
- Problema: Correos no se envían aunque la configuración SMTP sea correcta
- Solución: Revisar que las líneas `send_mail()` no estén comentadas en `views.py`

## CONFIGURACIÓN DE BASE DE DATOS

- PostgreSQL en Tembo Cloud
- Host: confidently-nifty-skylark.data-1.use1.tembo.io
- Nombre BD: postgres
- Usuario: postgres
- Contraseña: n5rNZneopwuKZiDd

## ENDPOINTS PRINCIPALES

- `/`: Página principal
- `/formulario/`: Formulario de solicitud
- `/login/`: Página de login
- `/admin-panel/`: Panel de solicitudes pendientes
- `/admin-panel/aprobadas/`: Panel de solicitudes aprobadas
- `/admin-panel/completadas/`: Panel de clientes con instalaciones completadas

## NOTAS IMPORTANTES

1. La autenticación utiliza sistema simple de sesiones (no usuarios de Django)
2. Las tablas de la base de datos fueron creadas manualmente y luego conectadas a Django
3. Se debe ejecutar `python create_all_django_tables.py` seguido de `python manage.py migrate --fake` para configurar correctamente la base de datos
4. El envío de correos utiliza SMTP con Gmail para envío real de notificaciones
