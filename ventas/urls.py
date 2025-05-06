from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, ProductViewSet, TransactionViewSet

router = DefaultRouter()
router.register(r'usuarios', UserViewSet)
router.register(r'productos', ProductViewSet)
router.register(r'transacciones', TransactionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
