from django.db import models


class Destino(models.Model):
    nombre=models.CharField(max_length=100, verbose_name='Nombre del destino')
    descripcion=models.TextField(verbose_name='Descripción del destino')
    imagen=models.ImageField(upload_to='destinos/', verbose_name='Imagen del destino')
    created=models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    updated=models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')
    autor=models.CharField(max_length=100, verbose_name='Autor de la reseña')
    calificacion=models.IntegerField(verbose_name='Calificación del destino')