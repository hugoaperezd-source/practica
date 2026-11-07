from django.shortcuts import render


def error_404(request, exception=None, mensaje=None):
    """Vista dedicada para renderizar la página personalizada de error 404."""
    detalle = mensaje or (str(exception) if exception else None)
    if not detalle:
        detalle = 'No se encontró ningún resultado válido para el parámetro de búsqueda solicitado.'

    context = {
        'mensaje_error': detalle,
        'ruta_solicitada': request.get_full_path(),
    }
    return render(request, 'errors/404.html', context, status=404)
