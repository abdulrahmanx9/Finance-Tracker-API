from rest_framework import serializers
from core.models import Transaction, Budget
from django.db.models import Sum
from .utils import fetch_exchange_rates
from decimal import Decimal


class TransactionSerializer(serializers.ModelSerializer):
    """Serializer for transaction models."""

    converted_amount = serializers.SerializerMethodField()
    converted_currency = serializers.SerializerMethodField()

    class Meta:
        model = Transaction
        fields = "__all__"
        read_only_fields = ["user"]

    def get_converted_currency(self, obj):
        return self.context["request"].user.userprofile.preferred_currency

    def get_converted_amount(self, obj):
        preferred_currency = self.get_converted_currency(obj)
        amount = obj.amount
        currency = obj.currency
        if currency == preferred_currency:
            return amount
        try:
            rates = fetch_exchange_rates(currency)
            rate = Decimal(str(rates[preferred_currency]))  # Convert float to Decimal
            converted = amount * rate
            return round(converted, 2)
        except (KeyError, Exception):
            # Fallback: return original amount if conversion fails
            return amount


class BudgetSerializer(serializers.ModelSerializer):
    """Serializer for budget models."""

    spent = serializers.SerializerMethodField()
    remaining = serializers.SerializerMethodField()

    class Meta:
        model = Budget
        fields = "__all__"
        read_only_fields = ["user"]

    def get_spent(self, obj):
        return (
            Transaction.objects.filter(
                user=obj.user,
                category=obj.category,
                transaction="expense",  # Only expenses count toward spending
                date__year=obj.month.year,  # Match the year
                date__month=obj.month.month,  # Match the month
            ).aggregate(Sum("amount"))["amount__sum"]
            or 0
        )

    def get_remaining(self, obj):
        return obj.limit - self.get_spent(obj)
