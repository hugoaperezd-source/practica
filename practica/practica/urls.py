"""
URL configuration for practica project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
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
# Importa la configuración global del proyecto (settings.py)
from django.conf import settings
# Importa el módulo de administración de Django
from django.contrib import admin
# Importa la función path para declarar las rutas URL
from django.urls import path

# Importa las vistas de la aplicación about
from about import views as about_views
# Importa las vistas de la aplicación contact
from contact import views as contact_views
# Importa las vistas de la aplicación core (inicio)
from core import views as core_views
# Importa las vistas de la aplicación errors (manejo de error 404)
from errors import views as errors_views
# Importa las vistas de la aplicación gallery (catálogo y filtros GET)
from gallery import views as gallery_views

# Lista principal de rutas URL del proyecto
urlpatterns = [
    # Ruta para acceder al panel de administración de Django
    path('admin/', admin.site.urls),
    # Ruta de la galería de destinos con soporte para filtros GET (?categoria= y ?zona=)
    path('gallery/', gallery_views.gallery, name='gallery'),
    # Ruta de la página de inicio (Home)
    path('', core_views.home, name='home'),
    # Ruta de la página "Acerca de nosotros" (About)
    path('about/', about_views.about, name='about'),
    # Ruta de la página del formulario de contacto
    path('contact/', contact_views.contact, name='contact'),
    # Ruta directa para visualizar la plantilla personalizada de error 404
    path('error-404/', errors_views.error_404, name='error_404'),
]

# Define el manejador global de Django para capturar cualquier error HTTP 404 con la app errors
handler404 = 'errors.views.error_404'

# Si el proyecto está en modo de desarrollo (DEBUG=True), sirve los archivos multimedia locales
if settings.DEBUG:
    # Importa la función static para servir imágenes subidas en desarrollo
    from django.conf.urls.static import static
    # Añade la configuración de MEDIA_URL y MEDIA_ROOT a las rutas disponibles
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
