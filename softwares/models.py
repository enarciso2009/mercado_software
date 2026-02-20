
from django.conf import settings
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
    comissao_percentual = models.DecimalField(max_digits=5, decimal_places=2, default=10)
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
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="interesses")
    mensagem = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="NOVO")
    criado_em = models.DateTimeField(auto_now_add=True)
    lido = models.BooleanField(default=False)
    resposta_vendedor = models.TextField(blank=True, null=True)
    respondido_em = models.DateTimeField(blank=True, null=True)


    def __str__(self):
        return f"{self.usuario.username} -> {self.software.nome}"



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



class Favorito(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    software = models.ForeignKey(Software, on_delete=models.CASCADE)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('usuario', 'software')


class MensagemInteresse(models.Model):
    interesse = models.ForeignKey(
        Interesse,
        on_delete=models.CASCADE,
        related_name="mensagens"
    )
    autor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    mensagem = models.TextField()
    criada_em = models.DateTimeField(auto_now_add=True)

    lida = models.BooleanField(default=False)

    class Meta:
        ordering = ["criada_em"]

    def __str__(self):
        return f"Mensagem de {self.autor} em {self.criada_em}"


class ContratoAceite(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    aceito = models.BooleanField(default=False)
    aceito_em = models.DateTimeField(null=True, blank=True)
    ip = models.GenericIPAddressField(null=True)


class Pedido(models.Model):
    STATUS_CHOICES = (
        ("PENDENTE", "Pendente"),
        ("PAGO", "Pago"),
        ("CANCELADO", "Cancelado"),
    )

    comprador = models.ForeignKey(User, on_delete=models.CASCADE, related_name="pedidos")
    software = models.ForeignKey(Software, on_delete=models.CASCADE)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDENTE")
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Pedido #{self.id}'


class Pagamento(models.Model):
    pedido = models.OneToOneField(Pedido, on_delete=models.CASCADE, related_name="pagamento")
    transaction_id = models.CharField(max_length=10, null=True, blank=True)
    status = models.CharField(max_length=50, null=True, blank=True)


class Avaliacao(models.Model):
    vendedor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="avaliacoes_recebidas")
    comprador = models.ForeignKey(User, on_delete=models.CASCADE, related_name="avaliacoes_feitas")
    nota = models.IntegerField()
    comentario = models.TextField(max_length=255, null=True, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("vendedor", "comprador")



