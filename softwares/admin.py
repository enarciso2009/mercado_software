from django.contrib import admin
from .models import Software, Categoria



@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nome", "ativa")
    prepopulated_fields = {"slug": ("nome",)}
    search_fields = ("nome",)

@admin.register(Software)
class SoftwareAdmin(admin.ModelAdmin):
    list_display = ("nome", "categoria", "preco", "ativo", "criado_em")
    list_filter = ("categoria", "ativo")
    search_fields = ("nome",)


