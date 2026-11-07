from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import get_object_or_404, render

from errors.views import error_404
from .models import Categoria, Destino, Zona

DESTINOS_POR_PAGINA = 5


def gallery(request):
    """Vista de galería con filtrado por etiquetas vía GET, control de error 404 y paginación."""
    destinos = Destino.objects.select_related('zona').prefetch_related('categorias')
    categorias = Categoria.objects.all()
    zonas = Zona.objects.all()

    categoria_id = request.GET.get('categoria')
    zona_id = request.GET.get('zona')
    categoria_actual = None
    zona_actual = None

    try:
        if categoria_id is not None:
            try:
                categoria_actual = get_object_or_404(Categoria, pk=int(categoria_id))
            except (ValueError, TypeError) as exc:
                raise Http404('El parámetro de categoría ingresado no es válido.') from exc

            destinos = destinos.filter(categorias=categoria_actual).distinct()
            if not destinos.exists():
                raise Http404('No se encontraron destinos para la categoría indicada.')

        if zona_id is not None:
            try:
                zona_actual = get_object_or_404(Zona, pk=int(zona_id))
            except (ValueError, TypeError) as exc:
                raise Http404('El parámetro de zona ingresado no es válido.') from exc

            destinos = destinos.filter(zona=zona_actual)
            if not destinos.exists():
                raise Http404('No se encontraron destinos para la zona indicada.')
    except Http404 as exc:
        return error_404(request, exception=exc, mensaje=str(exc))

    paginator = Paginator(destinos, DESTINOS_POR_PAGINA)
    page_number = request.GET.get('page')
    destinos_paginados = paginator.get_page(page_number)

    context = {
        'destinos': destinos_paginados,
        'categorias': categorias,
        'zonas': zonas,
        'categoria_actual': categoria_actual,
        'zona_actual': zona_actual,
    }
    return render(request, 'gallery/gallery.html', context)


