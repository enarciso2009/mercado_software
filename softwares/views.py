from django.shortcuts import render, get_object_or_404
from .models import Categoria, Software

def categoria_list(request):
    categorias = Categoria.objects.filter(ativa=True)
    context = {'categorias': categorias}

    return render(
        request,
        template_name = "softwares/categoria_list.html",
        context = context
    )

def software_list(request, slug):
    categoria = get_object_or_404(Categoria, slug=slug, ativa=True)
    softwares = categoria.softwares.filter(ativo=True)
    context = {
        'categoria': categoria,
        'softwares': softwares
    }
    return render(
        request,
        template_name = "softwares/software_list.html",
        context = context
    )

def software_detail(request, id):
    software = get_object_or_404(Software, id=id)
    context = {
        "software": software
    }
    return render(
        request,
        template_name = "softwares/software_detail.html",
        context = context
    )

