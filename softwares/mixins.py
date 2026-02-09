from django.core.exceptions import PermissionDenied

class VendedorRequiredMixin:

    def dispatch(self, request, *args, **kwargs):
        if request.user.perfil.tipo_usuario != 'VENDEDOR':
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)