from django import forms
from django.contrib.auth.models import User
from .models import Software, Interesse, Perfil, MensagemInteresse

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

class InteresseForm(forms.ModelForm):
    class Meta:
        model = Interesse
        fields = ["mensagem"]
        widgets = {
           "mensagem": forms.Textarea(attrs={"class": "form-control", "placeholder": "Mensagem (opcional)", "rows": 4}),
        }

class CadastroForm(forms.ModelForm):

    TIPO_USUARIO_CHOICES = (
        ('COMPRADOR', 'Quero comprar softwares'),
        ('VENDEDOR', 'Quero vender softwares'),
    )

    password1 = forms.CharField(label='Senha', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirme a senha', widget=forms.PasswordInput)
    tipo_usuario = forms.ChoiceField(choices=TIPO_USUARIO_CHOICES, widget=forms.RadioSelect, label="Você quer:")

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_password2(self):
        p1 = self.cleaned_data.get("password1")
        p2 = self.cleaned_data.get("password2")

        if p1 != p2:
            raise forms.ValidationError("As senhas não conferem.")
        return p2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])  # seta senha corretamente
        if commit:
            user.save()
            # cria profile automático
            Perfil.objects.create(user=user, tipo=self.cleaned_data["tipo_usuario"])
        return user


class RespostaInteresseForm(forms.ModelForm):
    class Meta:
        model = Interesse
        fields = ["resposta_vendedor"]


class MensagemInteresseForm(forms.BaseModelForm):
    class Meta:
        model = MensagemInteresse
        fields = ["mensagem"]
        widgets = {
            "mensagem": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Digite sua mensagem..."
            })
        }