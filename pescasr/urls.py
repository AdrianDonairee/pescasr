from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/usuarios/', include('users.urls')),
    path('api/', include('ventas.urls')),  # rutas de productos y transacciones
]
