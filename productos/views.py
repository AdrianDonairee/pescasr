from rest_framework import viewsets, permissions
from .models import Producto, Categoria
from .serializers import ProductoSerializer, CategoriaSerializer

class ProductoViewSet(viewsets.ModelViewSet):
    # traer categoria con select_related para que serializer tenga datos anidados sin N+1
    queryset = Producto.objects.select_related("categoria").all().order_by("id")
    serializer_class = ProductoSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all().order_by("nombre")
    serializer_class = CategoriaSerializer
    # permitir lectura pública para el frontend; si querés restringir modificaciones cambialo a IsAdminUser
    permission_classes = [permissions.AllowAny]