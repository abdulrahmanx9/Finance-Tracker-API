from django.db import models
from django.contrib.auth.models import User


class Transaction(models.Model):
    """Model for transaction."""

    TRANSACTION_TYPES = (
        ("expense", "Expense"),
        ("income", "Income"),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default="USD")
    category = models.CharField(max_length=50)
    transaction = models.CharField(max_length=7, choices=TRANSACTION_TYPES)
    date = models.DateTimeField()
    description = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ["-date"]


class Budget(models.Model):
    """Model for budget."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=50)
    limit = models.DecimalField(max_digits=10, decimal_places=2)
    month = models.DateField()

    class Mata:
        unique_together = ["user", "category", "month"]
