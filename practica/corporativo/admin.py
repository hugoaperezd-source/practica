# Importa el módulo de administración de Django
from django.contrib import admin

# Importa el modelo ParametroCorporativo de la app corporativo
from .models import ParametroCorporativo


@admin.register(ParametroCorporativo)
class ParametroCorporativoAdmin(admin.ModelAdmin):
    """Configuración personalizada del panel de administración para Parámetros Corporativos (8 atributos)."""

    # Atributo 1: Protege las fechas de creación y edición como solo lectura
    readonly_fields = ('created', 'updated')
    # Atributo 2: Columnas visibles en la tabla principal del administrador
    list_display = ('nombre', 'clave', 'valor', 'activo', 'updated')
    # Atributo 3: Panel lateral para filtrar por estado activo o fechas
    list_filter = ('activo', 'created', 'updated')
    # Atributo 4: Barra de búsqueda por nombre, clave o contenido del parámetro
    search_fields = ('nombre', 'clave', 'valor')
    # Atributo 5: Ordena los registros alfabéticamente por nombre
    ordering = ('nombre',)
    # Atributo 6: Barra de navegación jerárquica por fechas en la parte superior
    date_hierarchy = 'created'
    # Atributo 7: Permite editar el valor y el estado activo directamente desde la tabla
    list_editable = ('valor', 'activo')
    # Atributo 8: Muestra un máximo de 10 registros por página
    list_per_page = 10
    # Atributo 9: Agrupa los campos del formulario en secciones (Identificación y Auditoría)
    fieldsets = (
        ('Identificación del Parámetro', {
            'fields': ('clave', 'nombre', 'valor', 'activo'),
        }),
        ('Auditoría', {
            'fields': ('created', 'updated'),
            'classes': ('collapse',),
        }),
    )

