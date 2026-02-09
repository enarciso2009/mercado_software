from django.urls import path, include
from softwares.views import CustomLoginView

from .views import (
    CategoriaListView,
    SoftwareListByCategoriaView,
    SoftwareDetailView,
    SoftwareCreateView,
    SoftwareListAdminView,
    SoftwareUpdateView,
    SoftwareDeleteView,
    InteresseCreateView,
    InteresseListView,
    InteresseDetailView,
    CadastroView,
)

app_name = "softwares"

urlpatterns = [


    # LOGIN / CADASTRO
    path("login/", CustomLoginView.as_view(), name='login'),
    path("cadastro/", CadastroView.as_view(), name="cadastro"),

    #SITE PUBLICO
    path("", CategoriaListView.as_view(), name="categoria_list"),
    path("categoria/<slug:slug>/", SoftwareListByCategoriaView.as_view(), name="software_list"),
    path("softwares/<int:pk>/", SoftwareDetailView.as_view(), name="software_detail"),

    # ADMIN (vendedor)
    path("dashboard/softwares/", SoftwareListAdminView.as_view(), name="software_list_admin"),
    path("dashboard/softwares/novo/", SoftwareCreateView.as_view(), name="software_create"),
    path("dashboard/softwares/<int:pk>/editar/", SoftwareUpdateView.as_view(), name="software_update"),
    path("dashboard/softwares/<int:pk>/excluir/", SoftwareDeleteView.as_view(), name="software_delete"),

    # INTERESSE
    path("softwares/<int:pk>/interesse/", InteresseCreateView.as_view(), name="software_interesse"),
    path("dashboard/interesses/", InteresseListView.as_view(), name="interesse_list"),
    path("dashboard/interesses/<int:pk>/", InteresseDetailView.as_view(), name="interesse_detail"),



]