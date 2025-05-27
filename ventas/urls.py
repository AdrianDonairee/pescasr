from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, TransactionViewSet
from users.views import UserViewSet

router = DefaultRouter()
router.register(r'productos', ProductViewSet)
router.register(r'transacciones', TransactionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
