from rest_framework import viewsets, permissions
from rest_framework.permissions import SAFE_METHODS, BasePermission
from .models import Producto, Categoria
from .serializers import ProductoSerializer, CategoriaSerializer

class IsAdminOrReadOnly(BasePermission):
    """
    Allow read-only for anyone; only staff users can perform unsafe methods.
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated and request.user.is_staff)

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.select_related("categoria").all().order_by("id")
    serializer_class = ProductoSerializer
    permission_classes = [IsAdminOrReadOnly]

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all().order_by("nombre")
    serializer_class = CategoriaSerializer

    def get_permissions(self):
        # list/retrieve are public; create/update/delete require admin
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]