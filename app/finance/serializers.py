from rest_framework import serializers
from core.models import Transaction, Budget
from django.db.models import Sum


class TransactionSerializer(serializers.ModelSerializer):
    """Serializer for transaction models."""

    class Meta:
        model = Transaction
        fields = "__all__"
        read_only_fields = ["user"]


class BudgetSerializer(serializers.ModelSerializer):
    """Serializer for budget models."""

    spent = serializers.SerializerMethodField()
    remaining = serializers.SerializerMethodField()

    class Meta:
        model = Budget
        fields = "__all__"
        read_only_fields = ["user"]

    def get_spent(self, obj):
        return Transaction.objects.filter(
            user=obj.user,
            category=obj.category,
            transaction='expense',  # Only expenses count toward spending
            date__year=obj.month.year,   # Match the year
            date__month=obj.month.month  # Match the month
        ).aggregate(Sum('amount'))['amount__sum'] or 0

    def get_remaining(self, obj):
        return obj.limit - self.get_spent(obj)
