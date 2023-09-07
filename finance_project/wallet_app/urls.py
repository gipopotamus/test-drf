from django.urls import path
from . import views

urlpatterns = [
    # URL для регистрации
    path('register/', views.SignUpView.as_view(), name='register'),

    # URL для входа
    path('login/', views.CustomLoginView.as_view(), name='login'),

    # URL для выхода
    path('logout/', views.user_logout, name='logout'),

    # URL для списка всех транзакций
    path('transactions/', views.TransactionListView.as_view(), name='transactions_list'),

    # URL для добавления новой транзакции
    path('transactions/add/', views.TransactionCreateView.as_view(), name='add_transaction'),

    # URL для редактирования существующей транзакции
    path('transactions/<int:pk>/edit/', views.TransactionUpdateView.as_view(), name='edit_transaction'),

    # URL для удаления существующей транзакции
    path('transactions/<int:pk>/delete/', views.TransactionDeleteView.as_view(), name='delete_transaction'),

    # URL для списка всех категорий
    path('categories/', views.CategoryListView.as_view(), name='categories_list'),

    # URL для добавления новой категории
    path('categories/add/', views.CategoryCreateView.as_view(), name='add_category'),

    # URL для привязки транзакции к категории
    path('transactions/<int:transaction_id>/assign_category/<int:category_id>/', views.assign_category, name='assign_category'),

    # URL для отображения общего баланса кошелька
    path('wallet/balance/', views.wallet_balance, name='wallet_balance'),
]
