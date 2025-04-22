from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('ventas.urls')),  # Ahora se incluye el nuevo archivo de rutas de la app ventas
]
