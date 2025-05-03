# InterServices M - Plataforma de Servicios de Internet

Este proyecto consiste en una plataforma web para una empresa proveedora de servicios de internet, que incluye una página principal, un formulario de solicitud de servicio y un portal de inicio de sesión para clientes.

## Características

- **Página Principal**: Muestra información sobre la empresa, misión, visión y servicios ofrecidos
- **Formulario de Solicitud**: Permite a los usuarios solicitar un nuevo servicio de internet
- **Portal de Login**: Acceso para clientes existentes
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

6. **Aplicar migraciones**:
   ```bash
   python manage.py migrate --fake
   ```
   (Usamos --fake porque las tablas ya existen en PostgreSQL)

## Ejecución del Proyecto

Para iniciar el servidor de desarrollo:
```bash
python manage.py runserver
```

La aplicación estará disponible en:
- **Página Principal**: http://127.0.0.1:8000/
- **Formulario de Solicitud**: http://127.0.0.1:8000/formulario/
- **Portal de Login**: http://127.0.0.1:8000/login/
- **Panel de Administración**: http://127.0.0.1:8000/admin/

## Google Cloud Storage

Para habilitar el almacenamiento de archivos en Google Cloud Storage:

1. Crea un bucket en Google Cloud Storage llamado "interservicesm"
2. Habilita el acceso uniforme a nivel de bucket
3. Configura el bucket para acceso público si es necesario
4. Coloca el archivo de credenciales (`credentials.json`) en la raíz del proyecto
5. Asegúrate de que las credenciales tienen los permisos necesarios para el bucket
6. Las configuraciones de GCS ya están habilitadas en `settings.py`

## Estructura del Proyecto

- **proyecto/**: Configuración principal de Django
- **mi_app/**: Aplicación principal
  - **templates/mi_app/**: Plantillas HTML
    - **index.html**: Página principal
    - **formulario.html**: Formulario de solicitud
    - **login.html**: Portal de inicio de sesión
  - **models.py**: Modelos de datos
  - **views.py**: Lógica de vistas
  - **storage_utils.py**: Utilidades para almacenamiento de archivos

## Problemas Conocidos

- El modelo de datos debe adaptarse exactamente a la estructura de la tabla 'solicitudes' en PostgreSQL
- Al utilizar Google Cloud Storage con Uniform bucket-level access, no se pueden establecer ACLs individuales

## Notas para Desarrollo

- En entorno de desarrollo, los archivos se guardan localmente en las carpetas media/Cedulas/ y media/Factura_sp/
- Para agregar nuevas funcionalidades, extiende las vistas existentes en views.py
