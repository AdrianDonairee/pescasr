from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, register, login_view, logout_view, me

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('me/', me, name='me'),
]
