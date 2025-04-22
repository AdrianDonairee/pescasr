from rest_framework import viewsets
from .serializer import TransactionSerializer, CategorySerializer
from .models import Transaction, Category

class TransactionView(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()

class CategoryView(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
