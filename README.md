# Proyecto de Formulario de Registro con PostgreSQL y Google Cloud Storage

Este proyecto consiste en un formulario de registro para solicitudes de servicio de internet, integrado con PostgreSQL para el almacenamiento de datos y Google Cloud Storage para la gestión de archivos.

## Configuración del Entorno

1. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configurar variables de entorno**:
   - Copia `.env.template` a `.env`
   - Ajusta las variables según tu entorno

3. **Configurar Google Cloud Storage**:
   - Coloca el archivo `credentials.json` con las credenciales de Google Cloud en la raíz del proyecto
   - Para activar GCS, descomenta las líneas correspondientes en `settings.py`

## Base de Datos

El proyecto está configurado para conectarse a una base de datos PostgreSQL en Tembo Cloud. La estructura de la tabla `solicitudes` corresponde al modelo `Solicitud` definido en `models.py`.

Para aplicar migraciones a la base de datos existente:
```bash
python manage.py makemigrations
python manage.py migrate --fake
```

Se utiliza `--fake` porque la tabla ya existe en la base de datos.

## Almacenamiento de Archivos

Los archivos (fotos de cédula y recibos) se almacenan de la siguiente manera:
- **En desarrollo**: Localmente en las carpetas `media/Cedulas/` y `media/Factura_sp/`
- **En producción**: En Google Cloud Storage en las carpetas `Cedulas/` y `Factura_sp/`

Los archivos se nombran utilizando el número de cédula del solicitante como prefijo, seguido de un UUID único.

## Ejecución del Proyecto

Para iniciar el servidor de desarrollo:
```bash
python manage.py runserver
```

El formulario estará disponible en la URL: http://127.0.0.1:8000/formulario/

## Planes y Horarios

El formulario mantiene los tres planes originales (Básico, Estándar y Premium) que se mapean a los valores de la base de datos de la siguiente manera:
- **Plan Básico** → Internet 50MB
- **Plan Estándar** → Internet 100MB
- **Plan Premium** → Fibra Óptica 1GB

Los horarios se mapean así:
- **Mañana** → Mañana (8:00-12:00)
- **Tarde** → Tarde (13:00-17:00)
