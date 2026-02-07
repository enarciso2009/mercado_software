from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

class Categoria(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    ativa = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nome)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome


class Software(models.Model):

    TIPO_CHOICES = (
        ('PRONTO', 'Pronto'),
        ('SOB_DEMANDA', 'Sob_Demanda'),
    )

    nome = models.CharField(max_length=150)
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name="softwares")

    vendedor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="softwares")

    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome



