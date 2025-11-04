from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, TransactionViewSet, CartAPIView, OrderAPIView

router = DefaultRouter()
router.register(r'productos', ProductViewSet)
router.register(r'transacciones', TransactionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('cart/', CartAPIView.as_view(), name='cart'),
    path('orders/', OrderAPIView.as_view(), name='orders'),
]