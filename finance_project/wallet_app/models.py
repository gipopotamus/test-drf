from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(verbose_name='Категория',max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'


class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f({self.amount} - {self.category})