from django.db import models
from django.core.validators import RegexValidator

class Solicitud(models.Model):
    """
    Modelo para almacenar solicitudes de instalación de internet
    Coincide con la estructura de la tabla 'solicitudes' en PostgreSQL
    """
    ESTADO_CHOICES = [
        ('Pendiente', 'Pendiente'),
        ('En Proceso', 'En Proceso'),
        ('Completada', 'Completada'),
        ('Cancelada', 'Cancelada'),
    ]
    
    HORARIO_CHOICES = [
        ('Mañana (8:00-12:00)', 'Mañana (8:00-12:00)'),
        ('Tarde (13:00-17:00)', 'Tarde (13:00-17:00)'),
        ('Noche (18:00-20:00)', 'Noche (18:00-20:00)'),
    ]
    
    PLAN_CHOICES = [
        ('Internet 50MB', 'Internet 50MB'),
        ('Internet 100MB', 'Internet 100MB'),
        ('Internet 200MB', 'Internet 200MB'),
        ('Internet 500MB', 'Internet 500MB'),
        ('Fibra Óptica 1GB', 'Fibra Óptica 1GB'),
    ]
    
    # Mapeo para mostrar planes amigables en la interfaz
    PLAN_DISPLAY = {
        'Internet 50MB': 'Básico', 
        'Internet 100MB': 'Estándar',
        'Fibra Óptica 1GB': 'Premium'
    }
    
    # Campos básicos de información personal
    id_usuario = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    cedula = models.CharField(
        max_length=20, 
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^\d+$',
                message='La cédula debe contener solo números.',
                code='invalid_cedula'
            )
        ]
    )
    telefono = models.CharField(
        max_length=20,
        validators=[
            RegexValidator(
                regex=r'^\d+$',
                message='El número de teléfono debe contener solo números.',
                code='invalid_telefono'
            )
        ]
    )
    correo = models.EmailField()
    
    # Dirección y localización
    barrio = models.CharField(max_length=100)
    direccion = models.CharField(max_length=255)
    
    # Detalles del servicio
    plan_seleccionado = models.CharField(max_length=50, choices=PLAN_CHOICES)
    preferencia_horario = models.CharField(max_length=50, choices=HORARIO_CHOICES)
    
    # Enlaces a documentos
    url_cedula = models.URLField(max_length=500)
    url_recibo = models.URLField(max_length=500)
    
    # Información de seguimiento
    instalador = models.CharField(max_length=100, null=True, blank=True)
    fecha_instalacion = models.DateTimeField(null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='Pendiente')
    fecha_registro = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.cedula} - {self.estado}"
    
    def get_plan_display_name(self):
        """Devuelve el nombre amigable del plan para mostrar en la interfaz"""
        return self.PLAN_DISPLAY.get(self.plan_seleccionado, self.plan_seleccionado)
    
    class Meta:
        db_table = 'solicitudes'  # Nombre de la tabla en PostgreSQL
        verbose_name = 'Solicitud'
        verbose_name_plural = 'Solicitudes'

# Mantener el modelo Formulario para compatibilidad con el código existente si es necesario
class Formulario(models.Model):
    PLAN_CHOICES = [
        ('Básico', 'Plan Básico'),
        ('Estándar', 'Plan Estándar'),
        ('Premium', 'Plan Premium'),
    ]
    
    HORARIO_CHOICES = [
        ('Mañana', 'Mañana (8:00 AM - 12:00 PM)'),
        ('Tarde', 'Tarde (2:00 PM - 6:00 PM)'),
    ]
    
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    
    # Validadores para asegurar que solo se ingresen números
    cedula = models.CharField(
        max_length=20, 
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^\d+$',
                message='La cédula debe contener solo números.',
                code='invalid_cedula'
            )
        ]
    )
    
    correo = models.EmailField()
    direccion = models.CharField(max_length=200)
    barrio = models.CharField(max_length=100)
    
    # Validador para asegurar que el celular solo contenga números
    celular = models.CharField(
        max_length=20,
        validators=[
            RegexValidator(
                regex=r'^\d+$',
                message='El número de celular debe contener solo números.',
                code='invalid_celular'
            )
        ]
    )
    
    # Nuevos campos añadidos
    plan = models.CharField(max_length=20, choices=PLAN_CHOICES)
    horario = models.CharField(max_length=10, choices=HORARIO_CHOICES)
    
    foto_cedula = models.FileField(upload_to='documentos/cedulas/')
    recibo_publico = models.FileField(upload_to='documentos/recibos/')
    fecha_registro = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.nombres} {self.apellidos} - {self.cedula}"
