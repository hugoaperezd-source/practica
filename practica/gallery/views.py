from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Destino 


def gallery(request):
    destinos = Destino.objects.all()
    paginator=Paginator(destinos, 3)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    destinos = paginator.get_page(page_number)
    return render(request, 'gallery/gallery.html', {'destinos': destinos})



    