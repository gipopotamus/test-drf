from django.urls import path, include
from . import views

urlpatterns = [
    path('transactions/', views.TransactionListCreateAPIView.as_view(), name='transaction-list-create-api'),
    path('transactions/<int:pk>/', views.TransactionRetrieveUpdateDestroyAPIView.as_view(),
         name='transaction-detail-api'),
    path('categories/', views.CategoryListCreateAPIView.as_view(), name='category-list-create-api'),
    path('categories/<int:pk>/', views.CategoryRetrieveUpdateDestroyAPIView.as_view(), name='category-detail-api'),

    # Эндпоинт для получения итогового баланса кошелька
    path('wallet/balance/', views.WalletBalanceAPIView.as_view(), name='wallet-balance-api'),

    # Эндпоинт для привязки транзакции к категории
    path('transactions/<int:pk>/assign_category/<int:category_id>/', views.AssignCategoryAPIView.as_view(),
         name='assign-category-api'),

    path('register/', views.UserRegistrationAPIView.as_view(), name='user-registration'),

]
