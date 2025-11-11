# ventas/views.py
from rest_framework import viewsets, permissions
from rest_framework.exceptions import ValidationError
from .models import Product, Transaction
from .serializers import ProductSerializer, TransactionSerializer, CartItemSerializer
from decimal import Decimal
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction as db_transaction
from django.utils import timezone

# nuevo: importar el modelo real de productos
try:
    from productos.models import Producto as ProductoProd
except Exception:
    ProductoProd = None

# helper: si no existe Product en ventas, intentar crear espejo desde productos.Producto
def get_or_create_ventas_product_by_id(producto_id):
    """
    Return a ventas.Product instance for given producto_id.
    - If ventas.Product with pk exists -> return it.
    - Else, if productos.Producto exists -> create ventas.Product copy and return it.
    - Else -> raise Product.DoesNotExist
    """
    try:
        return Product.objects.get(pk=producto_id)
    except Product.DoesNotExist:
        # try to find in productos app and create a mirror
        if ProductoProd is None:
            raise
        try:
            prod_src = ProductoProd.objects.get(pk=producto_id)
        except ProductoProd.DoesNotExist:
            raise Product.DoesNotExist()
        # create ventas.Product mirror (minimal fields to match Product model)
        mirror = Product.objects.create(
            nombre=prod_src.nombre,
            descripcion=getattr(prod_src, "descripcion", "") or "",
            precio=getattr(prod_src, "precio", prod_src.precio),
            stock=getattr(prod_src, "stock", getattr(prod_src, "cantidad", 0)) or 0
        )
        return mirror


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


class CartAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # Obtener items del carrito del usuario (estado 'Carrito')
        items = Transaction.objects.filter(usuario=request.user, estado='Carrito')
        serialized = []
        for tx in items:
            prod = tx.producto
            serialized.append({
                "id": tx.id,
                "producto": {
                    "id": prod.id,
                    "nombre": prod.nombre,
                    "descripcion": prod.descripcion,
                    "precio": str(prod.precio),
                    "stock": prod.stock
                } if prod else None,
                "cantidad": tx.cantidad,
                "total": str(tx.total or (prod.precio * tx.cantidad) if prod else tx.total),
            })
        return Response(serialized, status=status.HTTP_200_OK)

    def post(self, request):
        # Espera body: { "items": [{ "producto_id": 1, "cantidad": 2 }, ...] }
        items = request.data.get("items")
        if items is None:
            return Response({"detail": "Missing items list"}, status=status.HTTP_400_BAD_REQUEST)

        # Validar items
        serializer = CartItemSerializer(data=items, many=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Borra items carrito existentes del usuario
        Transaction.objects.filter(usuario=request.user, estado='Carrito').delete()

        created = []
        for itm in serializer.validated_data:
            try:
                # ahora usamos helper que intenta crear espejo si hace falta
                prod = get_or_create_ventas_product_by_id(itm["producto_id"])
            except Product.DoesNotExist:
                return Response({"detail": f"Product {itm['producto_id']} not found"}, status=status.HTTP_400_BAD_REQUEST)
            cantidad = itm["cantidad"]
            total = (prod.precio * Decimal(cantidad))
            tx = Transaction.objects.create(
                usuario=request.user,
                producto=prod,
                cantidad=cantidad,
                total=total,
                fecha=None,
                estado='Carrito'
            )
            created.append({
                "id": tx.id,
                "producto": {
                    "id": prod.id,
                    "nombre": prod.nombre,
                    "descripcion": prod.descripcion,
                    "precio": str(prod.precio),
                    "stock": prod.stock
                },
                "cantidad": tx.cantidad,
                "total": str(tx.total),
            })

        return Response({"items": created}, status=status.HTTP_201_CREATED)


class OrderAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        """
        Espera: { "items": [ { "producto_id": 1, "cantidad": 2 }, ... ] }
        Crea Transaction(s) con estado='Pedido', descuenta stock y devuelve resumen.
        """
        items = request.data.get('items')
        if not isinstance(items, list):
            return Response({'detail': 'Missing items list'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = CartItemSerializer(data=items, many=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        created = []
        try:
            with db_transaction.atomic():
                for itm in serializer.validated_data:
                    try:
                        prod = get_or_create_ventas_product_by_id(itm['producto_id'])
                    except Product.DoesNotExist:
                        return Response({'detail': f"Product {itm['producto_id']} not found"}, status=status.HTTP_400_BAD_REQUEST)

                    cantidad = itm['cantidad']
                    if cantidad <= 0:
                        return Response({'detail': f"Cantidad inválida para producto {prod.id}"}, status=status.HTTP_400_BAD_REQUEST)

                    if prod.stock < cantidad:
                        return Response({'detail': f"No hay suficiente stock para {prod.nombre}"}, status=status.HTTP_400_BAD_REQUEST)

                    prod.stock -= cantidad
                    prod.save()

                    total = prod.precio * Decimal(cantidad)
                    tx = Transaction.objects.create(
                        usuario=request.user,
                        producto=prod,
                        cantidad=cantidad,
                        total=total,
                        fecha=timezone.now(),
                        estado='Pedido'
                    )
                    created.append({
                        'id': tx.id,
                        'producto_id': prod.id,
                        'cantidad': cantidad,
                        'total': str(total)
                    })
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'order_items': created}, status=status.HTTP_201_CREATED)
