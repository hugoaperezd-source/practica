# Importa la función render para mostrar plantillas HTML al usuario
from django.shortcuts import render


# Vista principal que renderiza la portada de inicio (Home)
def home(request):
    # Devuelve la respuesta HTTP con el template core/home.html
    return render(request, 'core/home.html')