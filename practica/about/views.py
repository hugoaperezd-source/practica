# Importa la función render para mostrar plantillas HTML al usuario
from django.shortcuts import render


# Vista que renderiza la sección institucional (About)
def about(request):
    # Devuelve la respuesta HTTP con el template about/about.html
    return render(request, 'about/about.html')