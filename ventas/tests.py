from django.test import TestCase
from .models import Product, Transaction
from users.models import User

class ProductTests(TestCase):
    def test_product_creation(self):
        product = Product.objects.create(
            nombre='Caña de pescar',
            descripcion='Caña de pescar profesional',
            precio=15000,
            stock=10
        )
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(product.nombre, 'Caña de pescar')
        self.assertEqual(product.stock, 10)

    def test_product_creation_invalid_precio(self):
        with self.assertRaises(Exception):
            Product.objects.create(
                nombre='Señuelo',
                descripcion='Señuelo básico',
                precio=-100,
                stock=5
            )

    def test_product_creation_invalid_stock(self):
        with self.assertRaises(Exception):
            Product.objects.create(
                nombre='Anzuelo',
                descripcion='Anzuelo resistente',
                precio=100,
                stock=-5
            )

    def test_product_update(self):
        product = Product.objects.create(
            nombre='Reel',
            descripcion='Reel de aluminio',
            precio=20000,
            stock=7
        )
        product.precio = 18000
        product.save()
        updated_product = Product.objects.get(nombre='Reel')
        self.assertEqual(updated_product.precio, 18000)

    def test_product_delete(self):
        product = Product.objects.create(
            nombre='Boya',
            descripcion='Boya flotante',
            precio=500,
            stock=20
        )
        product.delete()
        self.assertEqual(Product.objects.filter(nombre='Boya').count(), 0)

class TransactionTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='cliente', password='pass', email='cliente@test.com')
        self.product = Product.objects.create(
            nombre='Caña',
            descripcion='Caña básica',
            precio=1000,
            stock=5
        )

    def test_transaction_creation(self):
        trans = Transaction.objects.create(
            usuario=self.user,
            producto=self.product,
            cantidad=2,
            total=2000,
            estado='Pedido'
        )
        self.assertEqual(Transaction.objects.count(), 1)
        self.assertEqual(trans.cantidad, 2)
        self.assertEqual(trans.estado, 'Pedido')

    def test_transaction_creation_exceeds_stock(self):
        with self.assertRaises(Exception):
            Transaction.objects.create(
                usuario=self.user,
                producto=self.product,
                cantidad=10,  # mayor al stock disponible
                total=10000,
                estado='Pedido'
            )

    def test_transaction_state_change(self):
        trans = Transaction.objects.create(
            usuario=self.user,
            producto=self.product,
            cantidad=1,
            total=1000,
            estado='Pedido'
        )
        trans.estado = 'Completado'
        trans.save()
        updated_trans = Transaction.objects.get(id=trans.id)
        self.assertEqual(updated_trans.estado, 'Completado')

    def test_transaction_delete(self):
        trans = Transaction.objects.create(
            usuario=self.user,
            producto=self.product,
            cantidad=1,
            total=1000,
            estado='Pedido'
        )
        trans.delete()
        self.assertEqual(Transaction.objects.filter(id=trans.id).count(), 0)
