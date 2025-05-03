from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db import connection
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from django.http import JsonResponse
import json
from .models import Solicitud
from .storage_utils import guardar_archivo
import re
import random
import datetime

def index_view(request):
    """Vista para la página principal"""
    return render(request, 'mi_app/index.html')

def login_view(request):
    """Vista para la página de login"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Autenticación simple con usuario y contraseña fijos
        if username == 'default' and password == 'default':
            # Guardar alguna información en la sesión para indicar que está logueado
            request.session['is_admin'] = True
            request.session['admin_username'] = 'Admin'
            
            # Redirigir al panel de administración
            return redirect('admin_panel')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    
    return render(request, 'mi_app/login.html')

def logout_view(request):
    """Vista para cerrar sesión"""
    # Limpiar la sesión
    if 'is_admin' in request.session:
        del request.session['is_admin']
    if 'admin_username' in request.session:
        del request.session['admin_username']
    
    messages.success(request, 'Has cerrado sesión correctamente')
    return redirect('login')

def admin_required(view_func):
    """Decorador para verificar si el usuario es administrador"""
    def wrapper(request, *args, **kwargs):
        if request.session.get('is_admin', False):
            return view_func(request, *args, **kwargs)
        messages.error(request, 'Debes iniciar sesión como administrador para acceder a esta página')
        return redirect('login')
    return wrapper

@admin_required
def admin_panel(request):
    """Vista para el panel de administración - Solicitudes Pendientes"""
    # Obtener todas las solicitudes pendientes
    with connection.cursor() as cursor:
        cursor.execute("""
        SELECT id_usuario, nombre, apellido, cedula, telefono, correo,
               barrio, direccion, plan_seleccionado, preferencia_horario,
               url_cedula, url_recibo, instalador, fecha_instalacion, estado, fecha_registro
        FROM solicitudes
        WHERE estado = 'Pendiente'
        ORDER BY fecha_registro DESC
        """)
        columns = [col[0] for col in cursor.description]
        solicitudes_pendientes = [dict(zip(columns, row)) for row in cursor.fetchall()]
    
    # Paginación
    paginator = Paginator(solicitudes_pendientes, 10)  # 10 solicitudes por página
    page_number = request.GET.get('page', 1)
    solicitudes = paginator.get_page(page_number)
    
    context = {
        'solicitudes': solicitudes,
        'status': 'pendiente'
    }
    
    return render(request, 'mi_app/admin_panel.html', context)

@admin_required
def admin_panel_aprobadas(request):
    """Vista para el panel de administración - Solicitudes Aprobadas"""
    # Obtener todas las solicitudes aprobadas
    with connection.cursor() as cursor:
        cursor.execute("""
        SELECT id_usuario, nombre, apellido, cedula, telefono, correo,
               barrio, direccion, plan_seleccionado, preferencia_horario,
               url_cedula, url_recibo, instalador, fecha_instalacion, estado, fecha_registro
        FROM solicitudes
        WHERE estado = 'Aprobada'
        ORDER BY fecha_instalacion ASC
        """)
        columns = [col[0] for col in cursor.description]
        solicitudes_aprobadas = [dict(zip(columns, row)) for row in cursor.fetchall()]
    
    # Paginación
    paginator = Paginator(solicitudes_aprobadas, 10)  # 10 solicitudes por página
    page_number = request.GET.get('page', 1)
    solicitudes = paginator.get_page(page_number)
    
    context = {
        'solicitudes': solicitudes,
        'status': 'aprobada'
    }
    
    return render(request, 'mi_app/admin_panel.html', context)

@admin_required
def admin_panel_completadas(request):
    """Vista para el panel de administración - Solicitudes Completadas"""
    try:
        # Verificar si la tabla clientes existe
        with connection.cursor() as cursor:
            cursor.execute("SELECT to_regclass('clientes');")
            tabla_existe = cursor.fetchone()[0]
            
            if not tabla_existe:
                # Si la tabla no existe, mostrar un mensaje y una lista vacía
                messages.warning(request, "La tabla de clientes no existe todavía. No hay solicitudes completadas para mostrar.")
                return render(request, 'mi_app/admin_panel.html', {'solicitudes': [], 'status': 'completada'})
            
            # Si la tabla existe, obtener los clientes
            cursor.execute("""
            SELECT 
                id_cliente as id_usuario, 
                nombre, 
                apellido, 
                cedula, 
                telefono, 
                correo,
                barrio, 
                direccion, 
                plan_seleccionado, 
                preferencia_horario,
                url_cedula, 
                url_recibo, 
                'Completada' as estado, 
                fecha_registro
            FROM clientes
            ORDER BY fecha_registro DESC
            """)
            
            columns = [col[0] for col in cursor.description]
            clientes = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        # Paginación
        paginator = Paginator(clientes, 10)  # 10 clientes por página
        page_number = request.GET.get('page', 1)
        solicitudes = paginator.get_page(page_number)
        
        context = {
            'solicitudes': solicitudes,
            'status': 'completada'
        }
        
        return render(request, 'mi_app/admin_panel.html', context)
    
    except Exception as e:
        # En caso de error, mostrar un mensaje de error y una lista vacía
        messages.error(request, f"Error al obtener los clientes: {str(e)}")
        return render(request, 'mi_app/admin_panel.html', {'solicitudes': [], 'status': 'completada'})

@admin_required
def aprobar_solicitud(request, solicitud_id):
    """Vista para aprobar una solicitud"""
    if request.method == 'POST':
        # Obtener los datos del formulario
        instalador = request.POST.get('instalador')
        fecha_instalacion = request.POST.get('fecha_instalacion')
        imagenes_correctas = request.POST.get('imagenes_correctas') == 'on'
        
        # Verificar si se seleccionó que las imágenes son correctas
        if not imagenes_correctas:
            # Obtener información de la solicitud
            with connection.cursor() as cursor:
                cursor.execute("""
                SELECT nombre, apellido, correo, url_cedula, url_recibo
                FROM solicitudes
                WHERE id_usuario = %s
                """, [solicitud_id])
                result = cursor.fetchone()
                
                if result:
                    nombre, apellido, correo, url_cedula, url_recibo = result
                    
                    # Enviar correo informando del problema con las imágenes
                    subject = 'Problema con las imágenes de su solicitud - InterServicesSM'
                    message = f"""
                    Estimado/a {nombre} {apellido},
                    
                    Hemos detectado un problema con las imágenes proporcionadas en su solicitud de servicio.
                    
                    Por favor, envíe nuevamente las imágenes de su cédula y recibo de servicio público a través de nuestro formulario:
                    
                    http://tusitio.com/formulario/
                    
                    Lamentamos los inconvenientes.
                    
                    Atentamente,
                    El equipo de InterServicesSM
                    """
                    from_email = settings.DEFAULT_FROM_EMAIL
                    recipient_list = [correo]
                    
                    send_mail(subject, message, from_email, recipient_list)
                    
                    # Eliminar la solicitud
                    with connection.cursor() as cursor:
                        cursor.execute("""
                        DELETE FROM solicitudes
                        WHERE id_usuario = %s
                        """, [solicitud_id])
                    
                    messages.success(request, f'Se ha notificado al cliente sobre el problema con las imágenes y se ha eliminado la solicitud.')
                    return redirect('admin_panel')
        
        # Si las imágenes son correctas, aprobar la solicitud
        try:
            # Manejar correctamente la fecha y hora de instalación
            try:
                # Intentar parsear la fecha y hora
                fecha_instalacion_obj = None
                if fecha_instalacion:
                    # Si la entrada tiene formato datetime-local (YYYY-MM-DDThh:mm)
                    if 'T' in fecha_instalacion:
                        fecha_instalacion_obj = datetime.datetime.fromisoformat(fecha_instalacion)
                    # Si la entrada solo tiene fecha (YYYY-MM-DD)
                    else:
                        fecha_instalacion_obj = datetime.datetime.fromisoformat(f"{fecha_instalacion}T12:00:00")
                else:
                    # Si no se proporciona fecha, usar la fecha actual + 3 días a mediodía
                    fecha_instalacion_obj = datetime.datetime.now() + datetime.timedelta(days=3)
                    fecha_instalacion_obj = fecha_instalacion_obj.replace(hour=12, minute=0, second=0, microsecond=0)
                
                print(f"Fecha de instalación formateada: {fecha_instalacion_obj}")
            except Exception as e:
                # Si hay un error de formato, usar fecha actual + 3 días
                print(f"Error al formatear fecha: {str(e)}")
                fecha_instalacion_obj = datetime.datetime.now() + datetime.timedelta(days=3)
                fecha_instalacion_obj = fecha_instalacion_obj.replace(hour=12, minute=0, second=0, microsecond=0)
            
            # Actualizar la solicitud en la base de datos
            with connection.cursor() as cursor:
                cursor.execute("""
                UPDATE solicitudes
                SET instalador = %s, fecha_instalacion = %s, estado = 'Aprobada'
                WHERE id_usuario = %s
                """, [instalador, fecha_instalacion_obj, solicitud_id])
            
            # Obtener información para enviar correo
            with connection.cursor() as cursor:
                cursor.execute("""
                SELECT nombre, apellido, correo, plan_seleccionado, preferencia_horario
                FROM solicitudes
                WHERE id_usuario = %s
                """, [solicitud_id])
                result = cursor.fetchone()
                
                if result:
                    nombre, apellido, correo, plan, horario = result
                    
                    # Enviar correo de aprobación
                    subject = 'Su solicitud ha sido aprobada - InterServicesSM'
                    message = f"""
                    Estimado/a {nombre} {apellido},
                    
                    Nos complace informarle que su solicitud de servicio ha sido aprobada.
                    
                    Detalles de la instalación:
                    - Fecha y hora: {fecha_instalacion_obj.strftime('%d/%m/%Y %H:%M')}
                    - Técnico asignado: {instalador}
                    - Plan: {plan}
                    
                    Por favor, asegúrese de estar presente en la dirección proporcionada durante el horario de instalación.
                    
                    Atentamente,
                    El equipo de InterServicesSM
                    """
                    from_email = settings.DEFAULT_FROM_EMAIL
                    recipient_list = [correo]
                    
                    send_mail(subject, message, from_email, recipient_list)
            
            messages.success(request, f'Solicitud #{solicitud_id} aprobada correctamente y correo enviado al cliente.')
            return redirect('admin_panel')
            
        except Exception as e:
            messages.error(request, f'Error al aprobar la solicitud: {str(e)}')
            
    return redirect('admin_panel')

@admin_required
def rechazar_solicitud(request, solicitud_id):
    """Vista para rechazar una solicitud"""
    if request.method == 'POST':
        motivo_rechazo = request.POST.get('motivo_rechazo')
        
        # Obtener información de la solicitud
        with connection.cursor() as cursor:
            cursor.execute("""
            SELECT nombre, apellido, correo, url_cedula, url_recibo
            FROM solicitudes
            WHERE id_usuario = %s
            """, [solicitud_id])
            result = cursor.fetchone()
            
            if result:
                nombre, apellido, correo, url_cedula, url_recibo = result
                
                # Enviar correo de rechazo
                subject = 'Su solicitud ha sido rechazada - InterServicesSM'
                message = f"""
                Estimado/a {nombre} {apellido},
                
                Lamentamos informarle que su solicitud de servicio ha sido rechazada por el siguiente motivo:
                
                {motivo_rechazo}
                
                Si desea más información o volver a intentarlo, por favor contáctenos.
                
                Atentamente,
                El equipo de InterServicesSM
                """
                from_email = settings.DEFAULT_FROM_EMAIL
                recipient_list = [correo]
                
                send_mail(subject, message, from_email, recipient_list)
                
                # Eliminar la solicitud
                with connection.cursor() as cursor:
                    cursor.execute("""
                    DELETE FROM solicitudes
                    WHERE id_usuario = %s
                    """, [solicitud_id])
                
                messages.success(request, f'Solicitud #{solicitud_id} rechazada y eliminada correctamente. Se ha enviado un correo al cliente.')
                return redirect('admin_panel')
    
    messages.error(request, 'Se requiere un motivo para rechazar la solicitud.')
    return redirect('admin_panel')

@admin_required
def completar_solicitud(request, solicitud_id):
    """Vista para marcar una solicitud como completada"""
    if request.method == 'POST':
        # Obtener notas de instalación (opcional)
        notas_instalacion = request.POST.get('notas_instalacion', '')
        
        # Obtener los datos de la solicitud
        with connection.cursor() as cursor:
            cursor.execute("""
            SELECT nombre, apellido, cedula, telefono, correo, barrio, direccion,
                   plan_seleccionado, preferencia_horario, url_cedula, url_recibo,
                   instalador, fecha_instalacion
            FROM solicitudes
            WHERE id_usuario = %s
            """, [solicitud_id])
            result = cursor.fetchone()
            
            if result:
                nombre, apellido, cedula, telefono, correo, barrio, direccion, \
                plan, horario, url_cedula, url_recibo, instalador, fecha_instalacion = result
                
                try:
                    # Verificar si la tabla clientes existe
                    cursor.execute("SELECT to_regclass('clientes');")
                    tabla_existe = cursor.fetchone()[0]
                    
                    if not tabla_existe:
                        # Crear la tabla si no existe
                        cursor.execute("""
                        CREATE TABLE IF NOT EXISTS clientes (
                            id_cliente SERIAL PRIMARY KEY,
                            nombre VARCHAR(100) NOT NULL,
                            apellido VARCHAR(100) NOT NULL,
                            cedula VARCHAR(20) UNIQUE NOT NULL,
                            telefono VARCHAR(20) NOT NULL,
                            correo VARCHAR(254) NOT NULL,
                            barrio VARCHAR(100) NOT NULL,
                            direccion VARCHAR(255) NOT NULL,
                            plan_seleccionado VARCHAR(50) NOT NULL,
                            preferencia_horario VARCHAR(50) NOT NULL,
                            url_cedula VARCHAR(500) NOT NULL,
                            url_recibo VARCHAR(500) NOT NULL,
                            fecha_registro TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                        );
                        """)
                        connection.commit()
                    
                    # Insertar en la tabla clientes
                    cursor.execute("""
                    INSERT INTO clientes (
                        nombre, apellido, cedula, telefono, correo,
                        barrio, direccion, plan_seleccionado, preferencia_horario,
                        url_cedula, url_recibo
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, [
                        nombre, apellido, cedula, telefono, correo,
                        barrio, direccion, plan, horario,
                        url_cedula, url_recibo
                    ])
                    
                    # Enviar correo de contrato
                    subject = 'Contrato de Servicio - InterServicesSM'
                    fecha_instalacion_str = fecha_instalacion.strftime('%d/%m/%Y') if fecha_instalacion else "No disponible"
                    message = f"""
                    CONTRATO DE SERVICIO
                    
                    Estimado/a {nombre} {apellido},
                    
                    Nos complace confirmar que la instalación de su servicio ha sido completada exitosamente.
                    
                    DETALLES DEL SERVICIO:
                    - Cliente: {nombre} {apellido}
                    - Documento de Identidad: {cedula}
                    - Dirección: {direccion}, Barrio {barrio}
                    - Plan contratado: {plan}
                    - Fecha de instalación: {fecha_instalacion_str}
                    - Instalador: {instalador}
                    
                    {notas_instalacion if notas_instalacion else ''}
                    
                    Este correo sirve como comprobante de su contrato con InterServicesSM.
                    
                    Le agradecemos por confiar en nuestros servicios.
                    
                    Atentamente,
                    El equipo de InterServicesSM
                    """
                    from_email = settings.DEFAULT_FROM_EMAIL
                    recipient_list = [correo]
                    
                    send_mail(subject, message, from_email, recipient_list)
                    
                    # Eliminar la solicitud de la tabla solicitudes
                    cursor.execute("""
                    DELETE FROM solicitudes
                    WHERE id_usuario = %s
                    """, [solicitud_id])
                    
                    messages.success(request, f'Solicitud #{solicitud_id} marcada como completada. Cliente registrado y correo enviado.')
                    return redirect('admin_panel_aprobadas')
                    
                except Exception as e:
                    messages.error(request, f'Error al completar la solicitud: {str(e)}')
                    return redirect('admin_panel_aprobadas')
    
    messages.error(request, 'Error al completar la solicitud.')
    return redirect('admin_panel_aprobadas')

def formulario_view(request):
    """Vista para el formulario de solicitud de servicio"""
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

@admin_required
def dashboard_view(request):
    """Vista para el dashboard de métricas"""
    # Obtener estadísticas generales
    estadisticas = {}
    
    with connection.cursor() as cursor:
        # Contar solicitudes pendientes
        cursor.execute("SELECT COUNT(*) FROM solicitudes WHERE estado = 'Pendiente'")
        estadisticas['pendientes'] = cursor.fetchone()[0]
        
        # Contar solicitudes aprobadas
        cursor.execute("SELECT COUNT(*) FROM solicitudes WHERE estado = 'Aprobada'")
        estadisticas['aprobadas'] = cursor.fetchone()[0]
        
        # Contar clientes (instalaciones completadas)
        cursor.execute("SELECT to_regclass('clientes');")
        tabla_existe = cursor.fetchone()[0]
        
        if tabla_existe:
            cursor.execute("SELECT COUNT(*) FROM clientes")
            estadisticas['completadas'] = cursor.fetchone()[0]
        else:
            estadisticas['completadas'] = 0
        
        # Total de solicitudes procesadas (se asume que cada cliente completado tuvo una solicitud previa)
        estadisticas['total_procesadas'] = estadisticas['pendientes'] + estadisticas['aprobadas'] + estadisticas['completadas']
        
        # Distribución por planes (en solicitudes pendientes y aprobadas)
        cursor.execute("""
        SELECT plan_seleccionado, COUNT(*) as cantidad
        FROM solicitudes
        GROUP BY plan_seleccionado
        ORDER BY cantidad DESC
        """)
        planes_solicitudes = {}
        for row in cursor.fetchall():
            planes_solicitudes[row[0]] = row[1]
        
        # Distribución por planes (en clientes completados)
        if tabla_existe:
            cursor.execute("""
            SELECT plan_seleccionado, COUNT(*) as cantidad
            FROM clientes
            GROUP BY plan_seleccionado
            ORDER BY cantidad DESC
            """)
            planes_clientes = {}
            for row in cursor.fetchall():
                planes_clientes[row[0]] = row[1]
        else:
            planes_clientes = {}
        
        # Distribución por barrios (en todas las solicitudes)
        cursor.execute("""
        SELECT barrio, COUNT(*) as cantidad
        FROM solicitudes
        GROUP BY barrio
        ORDER BY cantidad DESC
        LIMIT 5
        """)
        barrios_solicitudes = {}
        for row in cursor.fetchall():
            barrios_solicitudes[row[0]] = row[1]
        
        # Distribución por barrios (en clientes completados)
        if tabla_existe:
            cursor.execute("""
            SELECT barrio, COUNT(*) as cantidad
            FROM clientes
            GROUP BY barrio
            ORDER BY cantidad DESC
            LIMIT 5
            """)
            barrios_clientes = {}
            for row in cursor.fetchall():
                barrios_clientes[row[0]] = row[1]
        else:
            barrios_clientes = {}
        
        # Solicitudes por mes (últimos 6 meses)
        cursor.execute("""
        SELECT 
            DATE_TRUNC('month', fecha_registro) as mes,
            COUNT(*) as cantidad
        FROM solicitudes
        WHERE fecha_registro >= CURRENT_DATE - INTERVAL '6 months'
        GROUP BY mes
        ORDER BY mes ASC
        """)
        solicitudes_por_mes = {}
        for row in cursor.fetchall():
            solicitudes_por_mes[row[0].strftime('%B %Y')] = row[1]
        
        # Instalaciones completadas por mes (últimos 6 meses)
        if tabla_existe:
            cursor.execute("""
            SELECT 
                DATE_TRUNC('month', fecha_registro) as mes,
                COUNT(*) as cantidad
            FROM clientes
            WHERE fecha_registro >= CURRENT_DATE - INTERVAL '6 months'
            GROUP BY mes
            ORDER BY mes ASC
            """)
            instalaciones_por_mes = {}
            for row in cursor.fetchall():
                instalaciones_por_mes[row[0].strftime('%B %Y')] = row[1]
        else:
            instalaciones_por_mes = {}
    
    # Preparar los datos para los gráficos en formato JSON
    import json
    
    # Gráfico circular: Estado de solicitudes
    datos_estado = [
        {'estado': 'Pendientes', 'cantidad': estadisticas['pendientes']},
        {'estado': 'Aprobadas', 'cantidad': estadisticas['aprobadas']},
        {'estado': 'Completadas', 'cantidad': estadisticas['completadas']}
    ]
    
    # Gráfico de barras: Distribución por planes
    datos_planes_solicitudes = [{'plan': k, 'cantidad': v} for k, v in planes_solicitudes.items()]
    datos_planes_clientes = [{'plan': k, 'cantidad': v} for k, v in planes_clientes.items()]
    
    # Gráfico de barras: Distribución por barrios
    datos_barrios_solicitudes = [{'barrio': k, 'cantidad': v} for k, v in barrios_solicitudes.items()]
    datos_barrios_clientes = [{'barrio': k, 'cantidad': v} for k, v in barrios_clientes.items()]
    
    # Gráfico de líneas: Solicitudes por mes
    datos_solicitudes_por_mes = [{'mes': k, 'cantidad': v} for k, v in solicitudes_por_mes.items()]
    datos_instalaciones_por_mes = [{'mes': k, 'cantidad': v} for k, v in instalaciones_por_mes.items()]
    
    context = {
        'estadisticas': estadisticas,
        'datos_estado': json.dumps(datos_estado),
        'datos_planes_solicitudes': json.dumps(datos_planes_solicitudes),
        'datos_planes_clientes': json.dumps(datos_planes_clientes),
        'datos_barrios_solicitudes': json.dumps(datos_barrios_solicitudes),
        'datos_barrios_clientes': json.dumps(datos_barrios_clientes),
        'datos_solicitudes_por_mes': json.dumps(datos_solicitudes_por_mes),
        'datos_instalaciones_por_mes': json.dumps(datos_instalaciones_por_mes)
    }
    
    return render(request, 'mi_app/dashboard.html', context)

def api_cliente(request, cedula):
    """
    Endpoint de API para obtener datos de un cliente por su número de cédula
    Retorna nombre, apellido, fecha de instalación y plan contratado
    URL: /api/cliente/<cedula>/
    Método: GET
    """
    try:
        # Verificar si es una solicitud GET
        if request.method != 'GET':
            return JsonResponse({"error": "Método no permitido"}, status=405)
        
        # Validar que la cédula contenga solo números
        if not cedula.isdigit():
            return JsonResponse({"error": "El número de cédula debe contener solo dígitos"}, status=400)
        
        # Buscar primero en la tabla de clientes (instalaciones completadas)
        with connection.cursor() as cursor:
            cursor.execute("""
            SELECT nombre, apellido, plan_seleccionado, fecha_registro
            FROM clientes
            WHERE cedula = %s
            """, [cedula])
            cliente = cursor.fetchone()
            
            if cliente:
                nombre, apellido, plan, fecha_registro = cliente
                # Formatear la fecha para la respuesta
                fecha_str = fecha_registro.strftime('%d/%m/%Y') if fecha_registro else "No disponible"
                
                return JsonResponse({
                    "nombre": nombre,
                    "apellido": apellido,
                    "plan_contratado": plan,
                    "fecha_instalacion": fecha_str
                })
            
            # Si no está en la tabla de clientes, buscar en solicitudes aprobadas
            cursor.execute("""
            SELECT nombre, apellido, plan_seleccionado, fecha_instalacion
            FROM solicitudes
            WHERE cedula = %s AND estado = 'Aprobada'
            """, [cedula])
            solicitud = cursor.fetchone()
            
            if solicitud:
                nombre, apellido, plan, fecha_instalacion = solicitud
                # Formatear la fecha para la respuesta
                fecha_str = fecha_instalacion.strftime('%d/%m/%Y') if fecha_instalacion else "Pendiente"
                
                return JsonResponse({
                    "nombre": nombre,
                    "apellido": apellido,
                    "plan_contratado": plan,
                    "fecha_instalacion": fecha_str,
                    "nota": "La instalación aún no ha sido completada"
                })
            
            # Si no está en ninguna tabla
            return JsonResponse({"error": "Cliente no encontrado"}, status=404)
            
    except Exception as e:
        print(f"Error en API: {str(e)}")
        return JsonResponse({"error": "Error interno del servidor"}, status=500)
