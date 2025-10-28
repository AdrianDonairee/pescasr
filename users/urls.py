from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import register, ProfileView, UserViewSet, logout

router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    # endpoints creados por el ViewSet (listar/crear/recuperar/actualizar usuarios)
    path('', include(router.urls)),

    # registro (function-based view existente en tu proyecto)
    path('register/', register, name='register'),

    # login -> POST {username, password} -> {access, refresh}
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),

    # refresh -> POST {refresh} -> {access}
    # Cambiado a 'refresh/' para que coincida con el cliente frontend (/users/refresh/)
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # logout (function-based view existente; debe aceptar POST con refresh si hace blacklist)
    path('logout/', logout, name='logout'),

    # perfil del usuario autenticado
    path('me/', ProfileView.as_view(), name='profile'),
]
