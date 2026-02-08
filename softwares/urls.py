from django.urls import path

from .views import (
    CategoriaListView,
    SoftwareListByCategoriaView,
    SoftwareDetailView,
    SoftwareCreateView,
    SoftwareListAdminView,
    SoftwareUpdateView,
    SoftwareDeleteView,
)

app_name = "softwares"

urlpatterns = [


    #SITE PUBLICO
    path("", CategoriaListView.as_view(), name="categoria_list"),
    path("categoria/<slug:slug>/", SoftwareListByCategoriaView.as_view(), name="software_list"),
    path("softwares/<int:pk>/", SoftwareDetailView.as_view(), name="software_detail"),

    # ADMIN
    path("dashboard/softwares/", SoftwareListAdminView.as_view(), name="software_list_admin"),
    path("dashboard/softwares/novo/", SoftwareCreateView.as_view(), name="software_create"),
    path("dashboard/softwares/<int:pk>/editar/", SoftwareUpdateView.as_view(), name="software_update"),
    path("dashboard/softwares/<int:pk>/excluir/", SoftwareDeleteView.as_view(), name="software_delete"),
]