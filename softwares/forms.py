from django import forms
from .models import Software

class SoftwareForm(forms.ModelForm):
    class Meta:
        model = Software
        fields = [
            "nome",
            "descricao",
            "preco",
            "tipo",
            "categoria",
            "imagem",
            "ativo",
        ]
