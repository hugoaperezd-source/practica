# Importa el módulo de administración de Django
from django.contrib import admin

# Importa los 3 modelos relacionados de la app gallery
from .models import Categoria, Destino, Zona

# Personaliza el título principal de la cabecera del panel de administración
admin.site.site_header = 'Administración de ViajAPP'
# Personaliza el subtítulo de la página de inicio del administrador
admin.site.index_title = 'Panel de Gestión de Ecoturismo y Destinos'
# Personaliza el título de la pestaña del navegador en el administrador
admin.site.site_title = 'ViajAPP Admin'


@admin.register(Zona)
class ZonaAdmin(admin.ModelAdmin):
    """Personalización del administrador para el modelo Zona (7 atributos)."""

    # 1. Campos de solo lectura (no editables manualmente)
    readonly_fields = ('created', 'updated')
    # 2. Columnas visibles en la tabla de listado de zonas
    list_display = ('nombre', 'descripcion', 'total_destinos', 'created', 'updated')
    # 3. Barra de búsqueda por nombre o descripción de la zona
    search_fields = ('nombre', 'descripcion')
    # 4. Panel lateral derecho de filtros por fechas
    list_filter = ('created', 'updated')
    # 5. Ordenamiento predeterminado por nombre
    ordering = ('nombre',)
    # 6. Navegación jerárquica por fechas en la parte superior
    date_hierarchy = 'created'
    # 7. Cantidad máxima de registros mostrados por página en el admin
    list_per_page = 10

    @admin.display(description='N° de Destinos')
    def total_destinos(self, obj):
        # Calcula y muestra cuántos destinos pertenecen a esta zona
        return obj.destinos.count()


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    """Personalización del administrador para el modelo Categoría (7 atributos)."""

    # 1. Campos de auditoría en modo solo lectura
    readonly_fields = ('created', 'updated')
    # 2. Columnas que se muestran en la lista de categorías
    list_display = ('nombre', 'total_destinos', 'created', 'updated')
    # 3. Cuadro de búsqueda por nombre de categoría
    search_fields = ('nombre',)
    # 4. Filtros laterales por fecha de creación y actualización
    list_filter = ('created', 'updated')
    # 5. Orden alfabético por nombre
    ordering = ('nombre',)
    # 6. Barra superior de navegación por fechas
    date_hierarchy = 'created'
    # 7. Paginación de 10 elementos por página
    list_per_page = 10

    @admin.display(description='Destinos Asociados')
    def total_destinos(self, obj):
        # Cuenta cuántos destinos tienen asignada esta categoría
        return obj.destinos.count()


@admin.register(Destino)
class DestinoAdmin(admin.ModelAdmin):
    """Personalización avanzada del administrador para Destino con 10 atributos."""

    # Atributo 1: Protege las fechas de creación y actualización como solo lectura
    readonly_fields = ('created', 'updated')
    # Atributo 2: Define las columnas visibles en la tabla del listado de destinos
    list_display = (
        'nombre',
        'zona',
        'autor',
        'calificacion',
        'mostrar_categorias',
        'created',
    )
    # Atributo 3: Agrega filtros laterales por zona, categorías, calificación y fecha
    list_filter = ('zona', 'categorias', 'calificacion', 'created')
    # Atributo 4: Habilita búsqueda por texto en campos propios y relaciones (zona y categoría)
    search_fields = (
        'nombre',
        'descripcion',
        'autor',
        'comentario',
        'zona__nombre',
        'categorias__nombre',
    )
    # Atributo 5: Ordena primero por mayor calificación y luego alfabéticamente por nombre
    ordering = ('-calificacion', 'nombre')
    # Atributo 6: Muestra barra de desglose por año/mes/día según fecha de creación
    date_hierarchy = 'created'
    # Atributo 7: Muestra un selector doble horizontal interactivo para asignar categorías (ManyToMany)
    filter_horizontal = ('categorias',)
    # Atributo 8: Permite editar la calificación directamente desde la tabla sin abrir el registro
    list_editable = ('calificacion',)
    # Atributo 9: Limita el listado a 10 registros por página
    list_per_page = 10
    # Atributo 10: Organiza el formulario de edición en secciones agrupadas (fieldsets)
    fieldsets = (
        ('Información del Destino', {
            'fields': ('nombre', 'descripcion', 'imagen', 'zona', 'categorias'),
        }),
        ('Reseña y Evaluación', {
            'fields': ('autor', 'comentario', 'calificacion'),
        }),
        ('Fechas de Registro', {
            'fields': ('created', 'updated'),
            'classes': ('collapse',),
        }),
    )

    @admin.display(description='Categorías / Etiquetas')
    def mostrar_categorias(self, obj):
        # Une con comas los nombres de todas las categorías asociadas al destino para mostrarlas en la tabla
        return ', '.join(cat.nombre for cat in obj.categorias.all())


