from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from finance.serializers import TransactionSerializer, BudgetSerializer
from core.models import Transaction, Budget
from django.db.models import Sum


class TransactionViewSet(viewsets.ModelViewSet):
    """View for managing transaction endpoint."""

    serializer_class = TransactionSerializer
    permission_classes = [
        IsAuthenticated,
    ]
    filterset_fields = ["category", "transaction", "date"]

    def get_queryset(self):
        """Filter with logged in user."""
        return Transaction.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Save to provided user."""
        serializer.save(user=self.request.user)


class BudgetViewSet(viewsets.ModelViewSet):
    """View for managing Budget endpoint."""

    serializer_class = BudgetSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    def get_queryset(self):
        """Filter with logged in user."""
        return Budget.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Save to provided user."""
        serializer.save(user=self.request.user)


class SummaryView(APIView):
    """View for providing a finance summary."""

    permission_classes = [IsAuthenticated]

    def get(self, request):

        user = self.request.user
        month = self.request.query_params.get("month")
        transactions = Transaction.objects.filter(user=user)
        # Filter by month if provided
        if month:
            year, month = month.split("-")
            transactions = transactions.filter(date__year=year, date__month=month)

        total_income = (
            transactions.filter(transaction="income").aggregate(Sum("amount"))[
                "amount__sum"
            ]
            or 0
        )
        total_expenses = (
            transactions.filter(transaction="expense").aggregate(Sum("amount"))[
                "amount__sum"
            ]
            or 0
        )
        net = total_income - total_expenses
        by_catagory = (
            transactions.filter(transaction="expense")
            .values("category")
            .annotate(total=Sum("amount"))
        )

        return Response(
            {
                "total_income": total_income,
                "total_expenses": total_expenses,
                "net": net,
                "by_catagory": {
                    item["category"]: item["total"] for item in by_catagory
                },
                "currency": "USD",
            }
        )
