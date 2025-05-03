"""
URL configuration for proyecto project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from mi_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Páginas públicas
    path('', views.index_view, name='index'),
    path('formulario/', views.formulario_view, name='formulario'),
    
    # Autenticación
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Panel de administración
    path('admin-panel/', views.admin_panel, name='admin_panel'),
    path('admin-panel/aprobadas/', views.admin_panel_aprobadas, name='admin_panel_aprobadas'),
    path('admin-panel/completadas/', views.admin_panel_completadas, name='admin_panel_completadas'),
    
    # Acciones de administración
    path('admin-panel/aprobar/<int:solicitud_id>/', views.aprobar_solicitud, name='aprobar_solicitud'),
    path('admin-panel/rechazar/<int:solicitud_id>/', views.rechazar_solicitud, name='rechazar_solicitud'),
    path('admin-panel/completar/<int:solicitud_id>/', views.completar_solicitud, name='completar_solicitud'),
]

# Añadir URLs para servir archivos media en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
