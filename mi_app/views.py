from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db import connection
from .models import Solicitud
from .storage_utils import guardar_archivo
import re
import random

def formulario_view(request):
    if request.method == 'POST':
        # Verificar que todos los campos requeridos estén presentes
        required_fields = [
            'nombres', 'apellidos', 'cedula', 'correo', 
            'direccion', 'barrio', 'celular', 'plan', 'horario'
        ]
        
        # Verificar campos de texto
        for field in required_fields:
            if not request.POST.get(field):
                messages.error(request, f'El campo {field} es obligatorio.')
                return render(request, 'mi_app/formulario.html')
        
        # Verificar archivos
        if not request.FILES.get('foto_cedula'):
            messages.error(request, 'Debe subir una foto de la cédula.')
            return render(request, 'mi_app/formulario.html')
            
        if not request.FILES.get('recibo_publico'):
            messages.error(request, 'Debe subir un recibo de servicio público.')
            return render(request, 'mi_app/formulario.html')
        
        # Validar que la cédula sea numérica
        cedula = request.POST.get('cedula')
        if not cedula.isdigit():
            messages.error(request, 'La cédula debe contener solo números.')
            return render(request, 'mi_app/formulario.html')
        
        # Validar que el celular sea numérico
        celular = request.POST.get('celular')
        if not celular.isdigit():
            messages.error(request, 'El número de celular debe contener solo números.')
            return render(request, 'mi_app/formulario.html')
        
        # Validar el plan seleccionado
        plan = request.POST.get('plan')
        valid_plans = ['Básico', 'Estándar', 'Premium']
        if plan not in valid_plans:
            messages.error(request, 'Por favor seleccione un plan válido.')
            return render(request, 'mi_app/formulario.html')
            
        # Mapeo de planes originales a nombres de BD
        plan_mapping = {
            'Básico': 'Internet 50MB',
            'Estándar': 'Internet 100MB',
            'Premium': 'Fibra Óptica 1GB'
        }
        
        # Validar el horario seleccionado
        horario = request.POST.get('horario')
        valid_horarios = ['Mañana', 'Tarde']
        if horario not in valid_horarios:
            messages.error(request, 'Por favor seleccione un horario válido.')
            return render(request, 'mi_app/formulario.html')
            
        # Mapeo de horarios originales a nombres de BD
        horario_mapping = {
            'Mañana': 'Mañana (8:00-12:00)',
            'Tarde': 'Tarde (13:00-17:00)'
        }
        
        # Procesar los datos del formulario
        try:
            # Obtener los datos básicos
            nombres = request.POST.get('nombres')
            apellidos = request.POST.get('apellidos')
            correo = request.POST.get('correo')
            direccion = request.POST.get('direccion')
            barrio = request.POST.get('barrio')
            foto_cedula = request.FILES.get('foto_cedula')
            recibo_publico = request.FILES.get('recibo_publico')
            
            # Subir los archivos a Google Cloud Storage o localmente según la configuración
            url_cedula = guardar_archivo(foto_cedula, cedula, 'Cedulas')
            url_recibo = guardar_archivo(recibo_publico, cedula, 'Factura_sp')
            
            # Generar un ID de usuario aleatorio que no exista en la base de datos
            # Este enfoque es temporal hasta que se resuelva el problema con la secuencia
            id_usuario_generado = generar_id_usuario_unico()
            
            print(f"Intentando crear solicitud con ID manual: {id_usuario_generado}")
            
            # Usar SQL directo con un ID generado manualmente
            with connection.cursor() as cursor:
                cursor.execute("""
                INSERT INTO solicitudes (
                    id_usuario, nombre, apellido, cedula, telefono, correo, 
                    barrio, direccion, plan_seleccionado, preferencia_horario,
                    url_cedula, url_recibo, estado, fecha_registro
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW()
                )
                """, [
                    id_usuario_generado, nombres, apellidos, cedula, celular, correo,
                    barrio, direccion, plan_mapping[plan], horario_mapping[horario],
                    url_cedula, url_recibo, 'Pendiente'
                ])
                
            print(f"Solicitud creada exitosamente con ID: {id_usuario_generado}")
            
            messages.success(request, "Formulario enviado correctamente, pronto recibirá un correo con la información de la instalación. ¡Gracias por registrarse!")
            return redirect('formulario')  # Redirigir a un formulario vacío
            
        except Exception as e:
            messages.error(request, f"Error al procesar el formulario: {str(e)}")
            print(f"Error detallado: {str(e)}")  # Log para depuración
    
    # Para la primera carga o después de un error
    context = {
        'form': {},  # Estructura vacía para compatibilidad con la plantilla
    }
    return render(request, 'mi_app/formulario.html', context)

def generar_id_usuario_unico():
    """
    Genera un ID de usuario único que no existe en la base de datos.
    """
    # Obtener el máximo ID actual
    max_id = 0
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT MAX(id_usuario) FROM solicitudes")
            result = cursor.fetchone()
            if result[0] is not None:
                max_id = result[0]
    except Exception as e:
        print(f"Error al obtener el máximo ID: {str(e)}")
        # Si hay un error, usar un número aleatorio grande
        return random.randint(1000, 10000)
    
    # Retornar el siguiente ID
    return max_id + 1
