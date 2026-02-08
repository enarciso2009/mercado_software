from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Categoria, Software
from .forms import SoftwareForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView


class CategoriaListView(ListView):
    model = Categoria
    template_name = "softwares/categoria_list.html"
    context_object_name = "categorias"

    def get_queryset(self):
        return Categoria.objects.filter(ativa=True)


class SoftwareListByCategoriaView(ListView):
    model = Software
    template_name = 'softwares/software_list.html'
    context_object_name = 'softwares'

    def get_queryset(self):
        self.categoria = get_object_or_404(
            Categoria,
            slug=self.kwargs['slug'],
            ativa=True
        )
        return self.categoria.softwares.filter(ativo=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categoria"] = self.categoria
        return context


class SoftwareDetailView(DetailView):
    model = Software
    template_name = 'softwares/software_detail.html'
    context_object_name = 'software'


class SoftwareCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Software
    form_class = SoftwareForm
    template_name = "softwares/software_form.html"
    success_url = reverse_lazy("softwares:software_list_admin")
    success_message = "Software cadastrado com sucesso!"

    def form_valid(self, form):
        form.instance.vendedor = self.request.user
        return super().form_valid(form)

class SoftwareListAdminView(LoginRequiredMixin, ListView):
    model = Software
    template_name = 'softwares/software_list_admin.html'
    context_object_name = 'softwares'
    paginate_by = 10


class SoftwareUpdateView(LoginRequiredMixin, UpdateView):
    model = Software
    form_class = SoftwareForm
    template_name = "softwares/software_form.html"
    success_url = reverse_lazy("softwares:software_list_admin")


class SoftwareDeleteView(LoginRequiredMixin, DeleteView):
    model = Software
    template_name = "softwares/software_confirm_delete.html"
    success_url = reverse_lazy("softwares:software_list_admin")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Software excluido com sucesso!")
        return super().delete(request, *args, **kwargs)
