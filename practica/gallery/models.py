from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Zona(models.Model):
    """Modelo que representa la zona geográfica de un destino turístico."""

    nombre = models.CharField(max_length=100, verbose_name='Nombre de la zona')
    descripcion = models.TextField(blank=True, verbose_name='Descripción de la zona')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    updated = models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')

    class Meta:
        verbose_name = 'Zona'
        verbose_name_plural = 'Zonas'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Categoria(models.Model):
    """Modelo que representa una categoría o etiqueta asociada a los destinos."""

    nombre = models.CharField(max_length=100, verbose_name='Nombre de la categoría')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    updated = models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')

    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Destino(models.Model):
    """Modelo principal de destinos turísticos relacionado con Zona (1:N) y Categoría (N:M)."""

    nombre = models.CharField(max_length=100, verbose_name='Nombre del destino')
    descripcion = models.TextField(verbose_name='Descripción del destino')
    imagen = models.ImageField(upload_to='destinos/', verbose_name='Imagen del destino')
    zona = models.ForeignKey(
        Zona,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='destinos',
        verbose_name='Zona geográfica',
    )
    categorias = models.ManyToManyField(
        Categoria,
        related_name='destinos',
        verbose_name='Categorías',
    )
    created = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    updated = models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')
    autor = models.CharField(max_length=100, verbose_name='Autor de la reseña')
    comentario = models.TextField(verbose_name='Comentario del destino')
    calificacion = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)],
        verbose_name='Calificación del destino',
    )

    class Meta:
        verbose_name = 'Destino'
        verbose_name_plural = 'Destinos'
        ordering = ['-created']

    def __str__(self):
        return self.nombre

