from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Categoria, Software

class CategoriaViewTest(TestCase):
    def setUp(self):
        self.categoria = Categoria.objects.create(
            nome="Gestão",
            slug="gestao",
            ativa=True
        )

    def test_categoria_list_status_code(self):
        response = self.client.get(reverse("softwares:categoria_list"))
        self.assertEqual(response.status_code, 200)

    def test_categoria_list_template(self):
        response = self.client.get(reverse("softwares:categoria_list"))
        self.assertTemplateUsed(response, "softwares/categoria_list.html")

    def test_categoria_aparece_na_pagina(self):
        response = self.client.get(reverse("softwares:categoria_list"))
        self.assertContains(response, "Gestão")


class SoftwareListViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="everton", password="123")

        # Corrigido o campo 'ativa' e adicionando slug
        self.categoria = Categoria(nome="RH", ativa=True)
        self.categoria.save()  # Gera automaticamente slug

        self.software = Software.objects.create(
            nome="Controle Financeiro",
            descricao="Sistema financeiro",
            preco=199.90,
            tipo="PRONTO",
            categoria=self.categoria,
            vendedor=self.user,
            ativo=True
        )

    def test_software_list_page(self):
        url = reverse("softwares:software_list", args=[self.categoria.slug])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Controle Financeiro")


class SoftwareDetailViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="everton", password="123")

        # Criando categoria com slug definido
        self.categoria = Categoria.objects.create(
            nome="RH",
            slug="rh",
            ativa=True
        )

        self.software = Software.objects.create(
            nome="Gestão de Pessoas",
            descricao="Sistema de RH",
            preco=299.90,
            tipo="PRONTO",
            categoria=self.categoria,
            vendedor=self.user,
            ativo=True
        )

    def test_software_detail_page(self):
        url = reverse("softwares:software_detail", args=[self.software.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Gestão de Pessoas")
        self.assertContains(response, "Sistema de RH")
