from rest_framework import serializers
from .models import Product, Transaction


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'nombre', 'descripcion', 'precio', 'stock']


class CartItemSerializer(serializers.Serializer):
    producto_id = serializers.IntegerField()
    cantidad = serializers.IntegerField(min_value=1)


class TransactionSerializer(serializers.ModelSerializer):
    producto = ProductSerializer(read_only=True)

    class Meta:
        model = Transaction
        fields = ['id', 'producto', 'cantidad', 'total', 'estado', 'fecha']
        read_only_fields = ['id', 'total', 'estado', 'fecha']