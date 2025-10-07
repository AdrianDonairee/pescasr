from django.db import models
from users.models import User





class Product(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()

    def clean(self):
        if self.precio < 0:
            raise ValidationError("El precio no puede ser negativo.")
        if self.stock < 0:
            raise ValidationError("El stock no puede ser negativo.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre


class Transaction(models.Model):
    ESTADOS = [
        ('Carrito', 'Carrito'),
        ('Pedido', 'Pedido'),
        ('Completado', 'Completado'),
        ('Cancelado', 'Cancelado')
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    producto = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)  # Producto solo si es Carrito
    cantidad = models.PositiveIntegerField(null=True, blank=True)  # Cantidad solo si es Carrito
    total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Total solo si es Pedido
    fecha = models.DateTimeField(null=True, blank=True)  # Fecha solo si es Pedido
    estado = models.CharField(max_length=20, choices=ESTADOS)

    def clean(self):
        if self.cantidad and self.producto:
            if self.cantidad > self.producto.stock:
                raise ValidationError("La cantidad no puede superar el stock disponible.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Transacción {self.id} - {self.usuario.nombre} - {self.estado}"

