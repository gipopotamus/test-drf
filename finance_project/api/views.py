from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from wallet_app.models import Transaction, Category
from .serializers import TransactionSerializer, CategorySerializer, UserRegistrationSerializer
from rest_framework.authtoken.models import Token


# Представление для создания и просмотра списка всех транзакций
class TransactionListCreateAPIView(generics.ListCreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# Представление для просмотра, обновления и удаления конкретной транзакции
class TransactionRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]


# Представление для создания и просмотра списка всех категорий
class CategoryListCreateAPIView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]


# Представление для просмотра, обновления и удаления конкретной категории
class CategoryRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]


# Представление для получения итогового баланса кошелька
class WalletBalanceAPIView(generics.ListAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        transactions = Transaction.objects.filter(user=user)
        return transactions

    def list(self, request, *args, **kwargs):
        transactions = self.get_queryset()
        total_income = transactions.filter(amount__gt=0).aggregate(total_income=models.Sum('amount'))['total_income'] or 0
        total_expense = transactions.filter(amount__lt=0).aggregate(total_expense=models.Sum('amount'))['total_expense'] or 0
        balance = total_income + total_expense
        return Response({'balance': balance})


# Представление для привязки транзакции к категории
class AssignCategoryAPIView(generics.UpdateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        category_id = self.kwargs.get('category_id')
        category = get_object_or_404(Category, pk=category_id)
        serializer.save(category=category)


class UserRegistrationAPIView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

