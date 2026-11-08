# Importa la función render para devolver la plantilla HTML junto con un código de estado HTTP
from django.shortcuts import render


def error_404(request, exception=None, mensaje=None):
    """Vista dedicada para renderizar la página personalizada de error 404."""
    # Toma el mensaje personalizado del filtro o el texto de la excepción capturada
    detalle = mensaje or (str(exception) if exception else None)
    # Si no se especificó un mensaje, asigna un mensaje explicativo por defecto
    if not detalle:
        detalle = 'No se encontró ningún resultado válido para el parámetro de búsqueda solicitado.'

    # Construye el diccionario de contexto con el mensaje y la URL exacta que causó el error
    context = {
        'mensaje_error': detalle,
        'ruta_solicitada': request.get_full_path(),
    }
    # Renderiza el template errors/404.html devolviendo explícitamente el código de estado HTTP 404
    return render(request, 'errors/404.html', context, status=404)

