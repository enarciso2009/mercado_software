from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from .utils import enviar_email_resposta, enviar_email_interesse
from .mixins import VendedorRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied
from .models import Categoria, Software, Interesse, Perfil, Favorito, MensagemInteresse
from .forms import SoftwareForm, InteresseForm, CadastroForm, RespostaInteresseForm, MensagemInteresseForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from django.utils import timezone




class CustomLoginView(LoginView):
    def get_success_url(self):
        user = self.request.user

        if user.perfil.tipo_usuario == "VENDEDOR":
            return '/dashboard/softwares/'
        return '/'


class CadastroView(FormView):
    template_name = "registration/cadastro.html"
    form_class = CadastroForm
    success_url = reverse_lazy("softwares:categoria_list")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data["password1"])
        user.save()

        # Atualiza perfil criado via signal

        perfil = user.perfil
        perfil.tipo_usuario = form.cleaned_data["tipo_usuario"]
        perfil.save()

        login(self.request, user)

        if perfil.tipo_usuario == 'VENDEDOR':
            return redirect('softwares:software_list_admin')

        return redirect('softwares:categoria_list')




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


class SoftwareCreateView(LoginRequiredMixin, VendedorRequiredMixin, SuccessMessageMixin, CreateView):
    model = Software
    form_class = SoftwareForm
    template_name = "softwares/software_form.html"
    success_url = reverse_lazy("softwares:software_list_admin")
    success_message = "Software cadastrado com sucesso!"

    def dispatch(self, request, *args, **kwargs):
        if request.user.perfil.tipo_usuario != 'VENDEDOR':
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.vendedor = self.request.user
        return super().form_valid(form)


class SoftwareListAdminView(LoginRequiredMixin, VendedorRequiredMixin, ListView):
    model = Software
    template_name = 'softwares/software_list_admin.html'
    context_object_name = 'softwares'
    paginate_by = 10
    def get_queryset(self):
        if self.request.user.perfil.tipo_usuario == "VENDEDOR":
            return Software.objects.filter(vendedor=self.request.user)
        return Software.objects.none() # Compradores não veem nada aqui


class SoftwareUpdateView(LoginRequiredMixin, VendedorRequiredMixin, UpdateView):
    model = Software
    form_class = SoftwareForm
    template_name = "softwares/software_form.html"
    success_url = reverse_lazy("softwares:software_list_admin")

    def get_queryset(self):
        # Garante que vendedor só edite seus próprios softwares
        return Software.objects.filter(vendedor=self.request.user)


class SoftwareDeleteView(LoginRequiredMixin, VendedorRequiredMixin, DeleteView):
    model = Software
    template_name = "softwares/software_confirm_delete.html"
    success_url = reverse_lazy("softwares:software_list_admin")

    def get_queryset(self):
        # Garante que o vendedor só exclua seus próprios softwares
        return Software.objects.filter(vendedor=self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Software excluido com sucesso!")
        return super().delete(request, *args, **kwargs)


class InteresseCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Interesse
    form_class = InteresseForm
    template_name = "softwares/interesse_form.html"
    success_message = "Seu interesse foi enviado com sucesso! Em breve o vendedor entrará em contato."

    def dispatch(self, request, *args, **kwargs):
        self.software = get_object_or_404(
            Software,
            pk=self.kwargs['pk'],
            ativo=True
        )
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.software = self.software
        form.instance.usuario = self.request.user
        response = super().form_valid(form)

        enviar_email_interesse(self.object)
        return response

    def get_success_url(self):
        return self.software.get_absolute_url() if hasattr(self.software, "get_absolute_url") else "/"


class InteresseListView(LoginRequiredMixin, VendedorRequiredMixin, ListView):
    model = Interesse
    template_name = "softwares/interesse_list.html"
    context_object_name = "interesses"
    paginate_by = 10

    def get_queryset(self):
        return Interesse.objects.filter(
            software__vendedor=self.request.user
        ).select_related("software")


class InteresseDetailView(LoginRequiredMixin, VendedorRequiredMixin, UpdateView):
    model = Interesse
    template_name = "softwares/interesse_detail.html"
    context_object_name = "interesse"
    form_class = RespostaInteresseForm

    def get_queryset(self):
        #garante que o vendedor só veja interesses dos próprios softwares
        return Interesse.objects.filter(
            software__vendedor=self.request.user
        )

    def get_object(self, queryset=None):
        interesse = super().get_object(queryset)

        if not interesse.lido:
            interesse.lido = True
            interesse.save(update_fields=["lido"])

        return interesse

    def form_valid(self, form):
        interesse = form.save(commit=False)
        interesse.status = 'RESPONDIDO'
        interesse.respondido_em = timezone.now()
        interesse.save()

        enviar_email_resposta(interesse)

        messages.success(self.request, "Resposta enviada com sucesso!")
        return redirect("softwares:interesse_list")


class FavoritoToggleView(LoginRequiredMixin, View):
    def post(self, request, pk):
        software = get_object_or_404(Software, pk=pk)
        favorito = Favorito.objects.filter(usuario=request.user, software=software)

        if favorito.exists():
            favorito.delete()
        else:
            Favorito.objects.create(
                usuario=request.user,
                software=software
            )
        return HttpResponseRedirect(software.get_absolute_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = MensagemInteresseForm()
        return context


class FavoritosListView(LoginRequiredMixin, ListView):
    model = Favorito
    template_name = "softwares/favoritos_list.html"
    context_object_name = 'favoritos'

    def get_queryset(self):
        return Favorito.objects.filter(usuario=self.request.user).select_related("software")


class MinhasSolicitacoesView(LoginRequiredMixin, ListView):
    model = Interesse
    template_name = "softwares/minhas_solicitacoes.html"

    def get_queryset(self):
        return Interesse.objects.filter(usuario=self.request.user).select_related("software")


class InteresseClienteDetailView(LoginRequiredMixin, DetailView):
    model = Interesse
    template_name = "softwares/interesse_cliente_detail.html"
    context_object_name = "interesse"

    def get_queryset(self):
        return Interesse.objects.filter(
            usuario=self.request.user
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = MensagemInteresseForm
        return context


class MensagemInteresseCreateView(LoginRequiredMixin, CreateView):
    model = MensagemInteresse
    form_class = MensagemInteresseForm

    def dispatch(self, request, *args, **kwargs):
        self.interesse = get_object_or_404(
            Interesse,
            pk=self.kwargs['pk']
        )

        # Só pode participar da conversa quem é comprador ou vendedor

        if request.user != self.interesse.usuario and \
            request.user != self.interesse.software.vendedor:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.interesse = self.interesse
        form.instance.autor = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        # Redireciona de volta para a página correta
        if self.request.user == self.interesse.usuario:
            return reverse_lazy("softwares:minha_solicitacao_detail", kwargs={"pk": self.interesse.pk})
        return reverse_lazy("softwares:interesse_detail", kwargs={"pk": self.interesse.pk})
