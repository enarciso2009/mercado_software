from django.urls import path
from . import views

app_name = 'softwares'

urlpatterns = [
    path("", views.categoria_list, name="categoria_list"),
    path("categoria/<slug:slug>/", views.software_list, name="software_list"),
    path("softwares/<int:id>/", views.software_detail, name="software_detail"),

]