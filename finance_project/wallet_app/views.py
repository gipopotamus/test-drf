from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Transaction, Category
from django.db import models


# Регистрация пользователя (используем обобщенный класс CreateView)
class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


# Вход пользователя
class CustomLoginView(LoginView):
    template_name = 'login.html'
    success_url = reverse_lazy('transactions_list')


# Выход пользователя
@login_required
def user_logout(request):
    logout(request)
    return redirect('login')


# Список всех транзакций
class TransactionListView(ListView):
    model = Transaction
    template_name = 'transactions_list.html'
    context_object_name = 'transactions'

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)


# Добавление новой транзакции
class TransactionCreateView(CreateView):
    model = Transaction
    template_name = 'add_transaction.html'
    fields = ['amount', 'category', 'description']
    success_url = reverse_lazy('transactions_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


# Редактирование существующей транзакции
class TransactionUpdateView(UpdateView):
    model = Transaction
    template_name = 'edit_transaction.html'
    fields = ['amount', 'category', 'description']
    success_url = reverse_lazy('transactions_list')


# Удаление существующей транзакции
class TransactionDeleteView(DeleteView):
    model = Transaction
    template_name = 'delete_transaction.html'
    success_url = reverse_lazy('transactions_list')


# Список всех категорий
class CategoryListView(ListView):
    model = Category
    template_name = 'categories_list.html'
    context_object_name = 'categories'


# Добавление новой категории
class CategoryCreateView(CreateView):
    model = Category
    template_name = 'add_category.html'
    fields = ['name']
    success_url = reverse_lazy('categories_list')


# Привязка транзакции к категории
@login_required
def assign_category(request, transaction_id, category_id):
    transaction = get_object_or_404(Transaction, pk=transaction_id, user=request.user)
    category = get_object_or_404(Category, pk=category_id)

    return redirect('transactions_list')


# Общий баланс кошелька
@login_required
def wallet_balance(request):
    # Рассчитайте общий баланс кошелька пользователя
    transactions = Transaction.objects.filter(user=request.user)
    total_income = transactions.filter(amount__gt=0).aggregate(total_income=models.Sum('amount'))['total_income'] or 0
    total_expense = transactions.filter(amount__lt=0).aggregate(total_expense=models.Sum('amount'))[
                        'total_expense'] or 0
    balance = total_income + total_expense

    return render(request, 'balance.html', {'balance': balance})
