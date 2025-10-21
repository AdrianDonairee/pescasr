# ventas/views.py
from rest_framework import viewsets, permissions
from rest_framework.exceptions import ValidationError
from .models import Product, Transaction
from .serializers import ProductSerializer, TransactionSerializer

class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user and request.user.is_staff:
            return True
        return getattr(obj, 'usuario', None) == request.user

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
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Transaction.objects.all()
        return Transaction.objects.filter(usuario=user)

    def perform_create(self, serializer):
        producto = serializer.validated_data.get('producto')
        cantidad = serializer.validated_data.get('cantidad') or 0
        if producto is None:
            raise ValidationError({'producto': 'Producto requerido.'})
        if cantidad <= 0:
            raise ValidationError({'cantidad': 'Cantidad debe ser > 0.'})
        if producto.stock < cantidad:
            raise ValidationError({'detail': 'No hay suficiente stock.'})
        producto.stock -= cantidad
        producto.save()
        serializer.save(usuario=self.request.user)
