# ventas/views.py
from rest_framework import viewsets, permissions
from .models import Product, Transaction
from .serializers import ProductSerializer, TransactionSerializer

class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Solo el dueño o admin puede ver/modificar su transacción
        return request.user.is_staff or obj.usuario == request.user

class ProductViewSet(viewsets.ModelViewSet):
    """
    Los productos son públicos para listar y ver detalle.
    Solo admin puede crear, actualizar o borrar productos.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]

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
        producto = serializer.validated_data.get('producto')
        cantidad = serializer.validated_data.get('cantidad', 0)
        if producto and cantidad:
            if producto.stock < cantidad:
                from rest_framework.exceptions import ValidationError
                raise ValidationError({'detail': 'No hay suficiente stock.'})
            producto.stock -= cantidad
            producto.save()
        serializer.save(usuario=self.request.user)
