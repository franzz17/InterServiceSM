from django.contrib import admin
from .models import Solicitud, Cliente, Formulario

@admin.register(Solicitud)
class SolicitudAdmin(admin.ModelAdmin):
    list_display = ('id_usuario', 'nombre', 'apellido', 'cedula', 'telefono', 'plan_seleccionado', 'estado', 'fecha_registro')
    list_filter = ('estado', 'plan_seleccionado', 'preferencia_horario', 'barrio')
    search_fields = ('nombre', 'apellido', 'cedula', 'telefono', 'correo')
    readonly_fields = ('fecha_registro',)
    fieldsets = (
        ('Información Personal', {
            'fields': ('nombre', 'apellido', 'cedula', 'telefono', 'correo')
        }),
        ('Dirección', {
            'fields': ('direccion', 'barrio')
        }),
        ('Detalles del Servicio', {
            'fields': ('plan_seleccionado', 'preferencia_horario')
        }),
        ('Documentos', {
            'fields': ('url_cedula', 'url_recibo')
        }),
        ('Estado de la Solicitud', {
            'fields': ('estado', 'instalador', 'fecha_instalacion', 'fecha_registro')
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        # Si es un objeto existente, hacemos algunos campos de solo lectura
        if obj:
            return ('fecha_registro', 'url_cedula', 'url_recibo', 'cedula')
        return ('fecha_registro',)

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('id_cliente', 'nombre', 'apellido', 'cedula', 'telefono', 'plan_seleccionado', 'fecha_registro')
    list_filter = ('plan_seleccionado', 'barrio')
    search_fields = ('nombre', 'apellido', 'cedula', 'telefono', 'correo')
    readonly_fields = ('fecha_registro',)
    fieldsets = (
        ('Información Personal', {
            'fields': ('nombre', 'apellido', 'cedula', 'telefono', 'correo')
        }),
        ('Dirección', {
            'fields': ('direccion', 'barrio')
        }),
        ('Detalles del Servicio', {
            'fields': ('plan_seleccionado', 'preferencia_horario')
        }),
        ('Documentos', {
            'fields': ('url_cedula', 'url_recibo')
        }),
        ('Información adicional', {
            'fields': ('fecha_registro',)
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        # Si es un objeto existente, hacemos algunos campos de solo lectura
        if obj:
            return ('fecha_registro', 'url_cedula', 'url_recibo', 'cedula')
        return ('fecha_registro',)

# Registrar también el modelo Formulario si es necesario
@admin.register(Formulario)
class FormularioAdmin(admin.ModelAdmin):
    list_display = ('nombres', 'apellidos', 'cedula', 'celular', 'plan', 'fecha_registro')
    list_filter = ('plan', 'horario', 'barrio')
    search_fields = ('nombres', 'apellidos', 'cedula', 'celular', 'correo')
    readonly_fields = ('fecha_registro',)
