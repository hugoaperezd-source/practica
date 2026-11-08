# Importa los modelos de gallery para calcular totales en tiempo real
from gallery.models import Categoria, Destino, Zona

# Importa el modelo ParametroCorporativo que almacena los datos de la agencia en la BD
from .models import ParametroCorporativo


def ctx_corporativo(request):
    """
    Procesador de contexto que inyecta datos operativos de la agencia
    (dirección, horario, contacto, emergencias forestales CONAF y métricas de destinos),
    sin ninguna relación con redes sociales.
    """
    # Inicializa el diccionario vacío que se inyectará globalmente en todas las plantillas HTML
    contexto = {}
    # Consulta únicamente los parámetros corporativos que estén marcados como activos en el Admin
    parametros = ParametroCorporativo.objects.filter(activo=True)
    # Recorre cada parámetro y asigna su 'clave' (ej. DIRECCION_OFICINA) con su respectivo 'valor'
    for parametro in parametros:
        contexto[parametro.clave] = parametro.valor

    # Agrega al contexto global el conteo dinámico de destinos, zonas y categorías registradas
    contexto['TOTAL_DESTINOS'] = Destino.objects.count()
    contexto['TOTAL_ZONAS'] = Zona.objects.count()
    contexto['TOTAL_CATEGORIAS'] = Categoria.objects.count()
    # Retorna el diccionario para que esté disponible en cualquier template sin pasarlo en cada vista
    return contexto

