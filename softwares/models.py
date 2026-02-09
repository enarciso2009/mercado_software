from django.db.models.signals import post_save
from django.dispatch import receiver


from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from PIL import Image

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

    imagem = models.ImageField(upload_to="softwares/", blank=True, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.imagem:
            img = Image.open(self.imagem.path)
            img.thumbnail((1200, 800))
            img.save(self.imagem.path, optimize=True, quality=80)


    vendedor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="softwares")

    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome


class Interesse(models.Model):
    STATUS_CHOICES = (
        ("NOVO", "Novo"),
        ("RESPONDIDO", "Respondido"),
    )

    software = models.ForeignKey(Software, on_delete=models.CASCADE, related_name="interesses")
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    mensagem = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="NOVO")
    criado_em = models.DateTimeField(auto_now_add=True)
    lido = models.BooleanField(default=False)

    def __str__(self):
        return f"Interesse em {self.software.nome} - {self.nome}"


class Perfil(models.Model):

    TIPO_USUARIO_CHOICES = (
        ('COMPRADOR', 'Comprador'),
        ('VENDEDOR', 'Vendedor'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    tipo_usuario = models.CharField(max_length=20, choices=TIPO_USUARIO_CHOICES)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} ({self.tipo_usuario})"



