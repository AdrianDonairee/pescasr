from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),

    # Endpoints JWT globales (opcionales)
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Cambiado a 'api/users/' para que coincida con el frontend (/api/users/...)
    path('api/users/', include('users.urls')),

    # Rutas de la app ventas
    path('api/', include('ventas.urls')),
]
