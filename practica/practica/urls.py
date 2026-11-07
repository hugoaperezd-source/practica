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
from django.conf import settings
from django.contrib import admin
from django.urls import path

from about import views as about_views
from contact import views as contact_views
from core import views as core_views
from errors import views as errors_views
from gallery import views as gallery_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('gallery/', gallery_views.gallery, name='gallery'),
    path('', core_views.home, name='home'),
    path('about/', about_views.about, name='about'),
    path('contact/', contact_views.contact, name='contact'),
    path('error-404/', errors_views.error_404, name='error_404'),
]

handler404 = 'errors.views.error_404'

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
