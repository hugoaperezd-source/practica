# Importa validadores de valor mínimo y máximo para restringir la calificación (0.0 a 5.0)
from django.core.validators import MaxValueValidator, MinValueValidator
# Importa el módulo models de Django para definir las tablas de la base de datos
from django.db import models


class Zona(models.Model):
    """Modelo 1: Representa la zona geográfica de un destino turístico (Relación 1 a N)."""

    # Campo de texto corto para el nombre de la zona (ej: Zona Norte, Zona Austral)
    nombre = models.CharField(max_length=100, verbose_name='Nombre de la zona')
    # Campo de texto largo opcional (blank=True) para describir la zona geográfica
    descripcion = models.TextField(blank=True, verbose_name='Descripción de la zona')
    # Guarda automáticamente la fecha y hora exacta en que se crea el registro
    created = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    # Actualiza automáticamente la fecha y hora cada vez que se modifica el registro
    updated = models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')

    class Meta:
        # Nombre singular y plural que se muestra en el panel de administración de Django
        verbose_name = 'Zona'
        verbose_name_plural = 'Zonas'
        # Ordena los registros alfabéticamente por nombre de forma predeterminada
        ordering = ['nombre']

    def __str__(self):
        # Devuelve el nombre de la zona como representación en texto del objeto
        return self.nombre


class Categoria(models.Model):
    """Modelo 2: Representa una categoría o etiqueta asociada a los destinos (Relación N a M)."""

    # Campo de texto corto para el nombre de la categoría/etiqueta (ej: Montaña, Lago, Playa)
    nombre = models.CharField(max_length=100, verbose_name='Nombre de la categoría')
    # Fecha de creación automática al insertar la categoría
    created = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    # Fecha de última actualización automática al editar la categoría
    updated = models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')

    class Meta:
        # Nombres visibles en el administrador de Django
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        # Ordena las categorías alfabéticamente por su nombre
        ordering = ['nombre']

    def __str__(self):
        # Devuelve el nombre de la categoría al representarla como cadena
        return self.nombre


class Destino(models.Model):
    """Modelo 3: Modelo principal de destinos turísticos relacionado con Zona (1:N) y Categoría (N:M)."""

    # Nombre del lugar turístico con máximo de 100 caracteres
    nombre = models.CharField(max_length=100, verbose_name='Nombre del destino')
    # Descripción detallada del destino turístico
    descripcion = models.TextField(verbose_name='Descripción del destino')
    # Imagen del destino almacenada dentro de la subcarpeta media/destinos/
    imagen = models.ImageField(upload_to='destinos/', verbose_name='Imagen del destino')
    # Relación Muchos-a-Uno (ForeignKey) con el modelo Zona: una Zona tiene muchos Destinos
    zona = models.ForeignKey(
        Zona,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='destinos',
        verbose_name='Zona geográfica',
    )
    # Relación Muchos-a-Muchos (ManyToManyField) con Categoria: un Destino tiene múltiples etiquetas
    categorias = models.ManyToManyField(
        Categoria,
        related_name='destinos',
        verbose_name='Categorías',
    )
    # Fecha y hora de creación del registro (solo se asigna al crearse)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    # Fecha y hora de última modificación del registro
    updated = models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')
    # Nombre del autor que escribió la reseña del destino
    autor = models.CharField(max_length=100, verbose_name='Autor de la reseña')
    # Opinión o reseña escrita sobre la experiencia en el destino
    comentario = models.TextField(verbose_name='Comentario del destino')
    # Calificación numérica decimal (ej: 4.5) validada entre 0.0 y 5.0 estrellas
    calificacion = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)],
        verbose_name='Calificación del destino',
    )

    class Meta:
        # Nombres visibles en el panel de administración
        verbose_name = 'Destino'
        verbose_name_plural = 'Destinos'
        # Ordena mostrando primero los destinos más recientes
        ordering = ['-created']

    def __str__(self):
        # Devuelve el nombre del destino como representación del objeto
        return self.nombre


