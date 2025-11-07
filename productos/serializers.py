from rest_framework import serializers
from .models import Producto, Categoria

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ["id", "nombre"]

class ProductoSerializer(serializers.ModelSerializer):
    # incluir categoria anidada en lecturas
    categoria = CategoriaSerializer(read_only=True)
    # aceptar categoria_id en escrituras (write_only mapea a campo categoria)
    categoria_id = serializers.PrimaryKeyRelatedField(
        queryset=Categoria.objects.all(),
        source="categoria",
        write_only=True,
        allow_null=True,
        required=False
    )

    class Meta:
        model = Producto
        fields = ["id", "nombre", "descripcion", "precio", "stock", "categoria", "categoria_id", "creado", "actualizado"]
        read_only_fields = ["id", "creado", "actualizado"]