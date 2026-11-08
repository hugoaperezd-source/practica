# Importa el módulo models de Django para definir la tabla de parámetros en la BD
from django.db import models


class ParametroCorporativo(models.Model):
    """Modelo para gestionar parámetros operativos, de atención y ecoturismo (sin relación con redes sociales)."""

    # Clave única tipo Slug (sin espacios) que se usa como nombre de variable en los templates (ej: DIRECCION_OFICINA)
    clave = models.SlugField(
        max_length=100,
        unique=True,
        verbose_name='Clave de contexto (identificador)',
    )
    # Nombre descriptivo del parámetro para identificarlo fácilmente en el panel Admin
    nombre = models.CharField(
        max_length=150,
        verbose_name='Nombre descriptivo del parámetro',
    )
    # Valor o texto real que se mostrará en las páginas del sitio web
    valor = models.CharField(
        max_length=300,
        verbose_name='Valor o contenido',
    )
    # Interruptor booleano para activar o desactivar el parámetro sin necesidad de borrarlo
    activo = models.BooleanField(
        default=True,
        verbose_name='Parámetro activo',
    )
    # Fecha y hora automática en que se creó el parámetro
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de creación',
    )
    # Fecha y hora automática de la última modificación del parámetro
    updated = models.DateTimeField(
        auto_now=True,
        verbose_name='Fecha de actualización',
    )

    class Meta:
        # Nombre singular y plural dentro del administrador de Django
        verbose_name = 'Parámetro Corporativo'
        verbose_name_plural = 'Parámetros Corporativos'
        # Ordena los parámetros alfabéticamente por su nombre descriptivo
        ordering = ['nombre']

    def __str__(self):
        # Muestra el nombre y la clave entre paréntesis al listar el objeto
        return f'{self.nombre} ({self.clave})'

