from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('ventas.urls')),  # Asegúrate de que el nombre coincida
]
