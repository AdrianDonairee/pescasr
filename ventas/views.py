# ventas/views.py
from rest_framework import viewsets, permissions
from .models import Product, Transaction
from .serializers import ProductSerializer, TransactionSerializer

class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Solo el dueño o admin puede ver/modificar su transacción
        return request.user.is_staff or obj.usuario == request.user

class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Los productos son públicos para listar y ver detalle.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]

class TransactionViewSet(viewsets.ModelViewSet):
    """
    Las transacciones solo son accesibles por usuarios logueados.
    Cada usuario ve sus transacciones; admin ve todas.
    """
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_staff:
            return qs
        return qs.filter(usuario=self.request.user)

    def perform_create(self, serializer):
        # Cuando se crea una transacción, asigna el usuario actual
        serializer.save(usuario=self.request.user)
