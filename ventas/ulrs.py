from django.urls import path, include
from rest_framework import routers
from ventas import views

router = routers.DefaultRouter()
router.register(r'categories', views.CategoryView, basename='categories')
router.register(r'transactions', views.TransactionView, basename='transactions')

urlpatterns = [
    path('dualcash/model/', include(router.urls))
]
