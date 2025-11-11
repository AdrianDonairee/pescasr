from rest_framework import serializers
from .models import Producto, Categoria

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ("id", "nombre")

class ProductoSerializer(serializers.ModelSerializer):
    # read: nested categoria object; write: accept categoria_id
    categoria = CategoriaSerializer(read_only=True)
    categoria_id = serializers.PrimaryKeyRelatedField(
        source="categoria",
        queryset=Categoria.objects.all(),
        write_only=True,
        allow_null=True,
        required=False,
    )

    class Meta:
        model = Producto
        fields = (
            "id",
            "nombre",
            "descripcion",
            "precio",
            "stock",
            "categoria",
            "categoria_id",
            "creado",
            "actualizado",
        )
        read_only_fields = ("id", "creado", "actualizado")