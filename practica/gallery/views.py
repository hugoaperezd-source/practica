# Importa Paginator para dividir los destinos en páginas
from django.core.paginator import Paginator
# Importa la excepción Http404 para lanzar errores de recurso no encontrado
from django.http import Http404
# Importa get_object_or_404 para buscar por ID o lanzar 404 automáticamente, y render para mostrar el HTML
from django.shortcuts import get_object_or_404, render

# Importa la vista personalizada error_404 desde nuestra app 'errors'
from errors.views import error_404
# Importa los 3 modelos relacionados de la app gallery
from .models import Categoria, Destino, Zona

# Constante que define cuántos destinos se muestran por cada página
DESTINOS_POR_PAGINA = 5


def gallery(request):
    """Vista de galería con filtrado por etiquetas vía GET, control de error 404 y paginación."""
    # Obtiene todos los destinos optimizando las consultas ForeignKey ('zona') y ManyToMany ('categorias')
    destinos = Destino.objects.select_related('zona').prefetch_related('categorias')
    # Obtiene todas las categorías para mostrarlas como botones de filtro en la plantilla
    categorias = Categoria.objects.all()
    # Obtiene todas las zonas geográficas para mostrarlas como botones de filtro en la plantilla
    zonas = Zona.objects.all()

    # Captura el parámetro 'categoria' enviado en la URL por método GET (ej: ?categoria=1)
    categoria_id = request.GET.get('categoria')
    # Captura el parámetro 'zona' enviado en la URL por método GET (ej: ?zona=2)
    zona_id = request.GET.get('zona')
    # Variables para recordar qué categoría o zona está activa actualmente en el filtro
    categoria_actual = None
    zona_actual = None

    try:
        # Si el usuario envió el parámetro 'categoria' por método GET:
        if categoria_id is not None:
            try:
                # Convierte el ID a entero y busca la categoría en la BD; si no existe, lanza Http404
                categoria_actual = get_object_or_404(Categoria, pk=int(categoria_id))
            except (ValueError, TypeError) as exc:
                # Si el parámetro no es un número (ej: ?categoria=abc), lanza Http404
                raise Http404('El parámetro de categoría ingresado no es válido.') from exc

            # Filtra los destinos que contengan la categoría seleccionada sin duplicados
            destinos = destinos.filter(categorias=categoria_actual).distinct()
            # Si la categoría existe pero no tiene ningún destino asociado, lanza Http404
            if not destinos.exists():
                raise Http404('No se encontraron destinos para la categoría indicada.')

        # Si el usuario envió el parámetro 'zona' por método GET:
        if zona_id is not None:
            try:
                # Convierte el ID a entero y busca la zona en la BD; si no existe, lanza Http404
                zona_actual = get_object_or_404(Zona, pk=int(zona_id))
            except (ValueError, TypeError) as exc:
                # Si el parámetro no es un número (ej: ?zona=xyz), lanza Http404
                raise Http404('El parámetro de zona ingresado no es válido.') from exc

            # Filtra los destinos que pertenecen a la zona geográfica seleccionada
            destinos = destinos.filter(zona=zona_actual)
            # Si la zona no tiene destinos asociados, lanza Http404
            if not destinos.exists():
                raise Http404('No se encontraron destinos para la zona indicada.')
    except Http404 as exc:
        # Si ocurrió cualquier error 404 al filtrar, delega la respuesta a la app 'errors' con status=404
        return error_404(request, exception=exc, mensaje=str(exc))

    # Crea el paginador dividiendo la lista de destinos de 5 en 5
    paginator = Paginator(destinos, DESTINOS_POR_PAGINA)
    # Obtiene el número de página actual desde el parámetro GET (?page=...)
    page_number = request.GET.get('page')
    # Obtiene los objetos correspondientes a la página solicitada
    destinos_paginados = paginator.get_page(page_number)

    # Diccionario de contexto que se envía a la plantilla gallery.html
    context = {
        'destinos': destinos_paginados,
        'categorias': categorias,
        'zonas': zonas,
        'categoria_actual': categoria_actual,
        'zona_actual': zona_actual,
    }
    # Renderiza la plantilla gallery/gallery.html con los datos filtrados y paginados
    return render(request, 'gallery/gallery.html', context)



