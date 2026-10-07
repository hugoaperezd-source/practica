from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Destino(models.Model):
    nombre=models.CharField(max_length=100, verbose_name='Nombre del destino')
    descripcion=models.TextField(verbose_name='Descripción del destino')
    imagen=models.ImageField(upload_to='destinos/', verbose_name='Imagen del destino')
    created=models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    updated=models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')
    autor=models.CharField(max_length=100, verbose_name='Autor de la reseña')
    comentario=models.TextField(verbose_name='Comentario del destino')
    calificacion=models.DecimalField(max_digits=2, decimal_places=1, validators=[MinValueValidator(0.0), MaxValueValidator(5.0)], verbose_name='Calificación del destino')


    class Meta:
        verbose_name='Destino'
        verbose_name_plural='Destinos'

    def __str__(self):
        return self.nombre