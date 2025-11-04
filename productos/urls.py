from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import ProductoViewSet, CategoriaViewSet

router = DefaultRouter()
router.register(r"productos", ProductoViewSet, basename="producto")
router.register(r"categorias", CategoriaViewSet, basename="categoria")

urlpatterns = [
    path("", include(router.urls)),
]