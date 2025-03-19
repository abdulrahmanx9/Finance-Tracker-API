from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from serializers import TransactionSerializer
from core.models import Transaction


class TransactionViewSet(viewsets.ModelViewSet):
    """View for managing transaction API."""

    serializer_class = TransactionSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    def get_queryset(self):
        """Filter with logged in user."""
        return Transaction.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Save to provided user."""
        serializer.save(user=self.request.user)
