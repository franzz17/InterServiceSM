from google.cloud import storage
import os
import uuid

def subir_archivo(archivo, cedula, tipo_documento):
    """
    Sube un archivo al bucket de Google Cloud Storage
    
    Args:
        archivo: Archivo cargado desde el formulario Django
        cedula: Número de cédula para incluir en el nombre del archivo
        tipo_documento: Tipo de documento ('Cedulas' o 'Factura_sp')
    
    Returns:
        URL pública del archivo subido
    """
    from django.conf import settings
    
    try:
        # Verificar que existan las credenciales
        credentials_path = settings.GS_CREDENTIALS
        if not os.path.exists(credentials_path):
            print(f"Advertencia: No se encontró el archivo de credenciales en {credentials_path}")
            raise Exception(f"Archivo de credenciales no encontrado en {credentials_path}")
        
        # Configurar la variable de entorno para Google Cloud
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path
        
        # Nombre del bucket
        bucket_name = settings.GS_BUCKET_NAME
        
        # Generar un nombre único para el archivo
        extension = os.path.splitext(archivo.name)[1].lower()  # Obtener la extensión en minúsculas
        nombre_archivo_destino = f"{cedula}_{uuid.uuid4()}{extension}"
        
        # Ruta destino en el bucket (carpeta/archivo)
        ruta_destino = f"{tipo_documento}/{nombre_archivo_destino}"
        
        print(f"Intentando subir archivo a GCS: {ruta_destino}")
        
        # Inicializar cliente de GCS
        client = storage.Client()
        bucket = client.bucket(bucket_name)
        
        # Crear un blob y subir el archivo
        blob = bucket.blob(ruta_destino)
        
        # Asegurarse de que el archivo esté en la posición inicial
        archivo.seek(0)
        
        # Subir el archivo
        blob.upload_from_file(archivo, content_type=archivo.content_type)
        
        # No intentar establecer ACLs individuales ya que Uniform bucket-level access está habilitado
        # La visibilidad pública se maneja a nivel de bucket
        
        # Generar URL pública (asumiendo que el bucket es público)
        url_publica = f"https://storage.googleapis.com/{bucket_name}/{ruta_destino}"
        
        print(f"Archivo subido exitosamente a GCS. URL: {url_publica}")
        
        return url_publica
        
    except Exception as e:
        print(f"Error detallado al subir archivo a GCS: {str(e)}")
        raise Exception(f"Error al subir archivo a Google Cloud Storage: {str(e)}")

def modo_desarrollo_guardar_archivo(archivo, cedula, tipo_documento):
    """
    Guarda el archivo localmente cuando estamos en entorno de desarrollo
    
    Args:
        archivo: Archivo cargado desde el formulario Django
        cedula: Número de cédula para incluir en el nombre del archivo
        tipo_documento: Tipo de documento ('Cedulas' o 'Factura_sp')
    
    Returns:
        Ruta relativa del archivo guardado
    """
    from django.conf import settings
    
    # Determinar la carpeta destino
    carpeta_destino = os.path.join(settings.MEDIA_ROOT, tipo_documento)
    
    # Crear la carpeta si no existe
    if not os.path.exists(carpeta_destino):
        os.makedirs(carpeta_destino)
    
    # Generar un nombre único para el archivo
    extension = os.path.splitext(archivo.name)[1]  # Obtener la extensión del archivo original
    nombre_archivo = f"{cedula}_{uuid.uuid4()}{extension}"
    
    # Ruta completa del archivo
    ruta_completa = os.path.join(carpeta_destino, nombre_archivo)
    
    # Guardar el archivo
    with open(ruta_completa, 'wb+') as destination:
        for chunk in archivo.chunks():
            destination.write(chunk)
    
    # Retornar la URL relativa para acceder al archivo
    return f"{settings.MEDIA_URL}{tipo_documento}/{nombre_archivo}"

def guardar_archivo(archivo, cedula, tipo_documento):
    """
    Función principal para guardar archivos, que decide si usar Google Cloud Storage
    o almacenamiento local según la configuración.
    
    Args:
        archivo: Archivo cargado desde el formulario Django
        cedula: Número de cédula para incluir en el nombre del archivo
        tipo_documento: Tipo de documento ('Cedulas' o 'Factura_sp')
    
    Returns:
        URL del archivo guardado
    """
    from django.conf import settings
    
    # Verificar si estamos usando Google Cloud Storage
    try:
        use_gcs = hasattr(settings, 'DEFAULT_FILE_STORAGE') and 'gcloud' in settings.DEFAULT_FILE_STORAGE
        print(f"¿Usar Google Cloud Storage? {use_gcs}")
        
        if use_gcs:
            # Usar Google Cloud Storage
            return subir_archivo(archivo, cedula, tipo_documento)
        else:
            # Usar almacenamiento local (desarrollo)
            return modo_desarrollo_guardar_archivo(archivo, cedula, tipo_documento)
    except Exception as e:
        print(f"Error al guardar archivo: {str(e)}. Usando almacenamiento local.")
        # En caso de error, intentar con almacenamiento local
        return modo_desarrollo_guardar_archivo(archivo, cedula, tipo_documento)
