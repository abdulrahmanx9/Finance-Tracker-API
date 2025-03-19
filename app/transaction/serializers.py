from rest_framework import serializers
from core.models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    """Serializer for transaction models."""

    model = Transaction
    fields = "__all__"
    read_only_fields = ["user"]
