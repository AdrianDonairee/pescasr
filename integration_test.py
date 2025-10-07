from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User
from ventas.models import Product, Transaction

class IntegrationTests(APITestCase):
    def test_full_purchase_flow(self):
        # Registro de usuario
        register_url = reverse('register')
        user_data = {
            "username": "integracion",
            "email": "integra@test.com",
            "password": "testpass"
        }
        response = self.client.post(register_url, user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Login de usuario
        login_url = reverse('login')
        login_data = {
            "username": "integracion",
            "password": "testpass"
        }
        response = self.client.post(login_url, login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Crear producto
        product = Product.objects.create(
            nombre="Combo pesca",
            descripcion="Combo caña y reel",
            precio=5000,
            stock=5
        )

        # Comprar producto (crear transacción)
        user = User.objects.get(username="integracion")
        purchase_url = reverse('transaction-list')  # <-- corregido
        purchase_data = {
            "usuario": user.id,
            "producto": product.id,
            "cantidad": 2,
            "total": 10000,
            "estado": "Pedido"
        }
        self.client.force_authenticate(user=user)
        response = self.client.post(purchase_url, purchase_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Verificar que el stock se actualizó
        product.refresh_from_db()
        self.assertEqual(product.stock, 3)

        # Verificar que la transacción está asociada al usuario
        trans = Transaction.objects.get(usuario=user, producto=product)
        self.assertEqual(trans.cantidad, 2)
        self.assertEqual(trans.estado, "Pedido")