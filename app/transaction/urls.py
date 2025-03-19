from rest_framework.routers import DefaultRouter
from django.urls import path, include
from views import TransactionViewSet

router = DefaultRouter()
router.register(r"transaction", TransactionViewSet, basename="transactions")

url_patterns = [
    path("", include(router.urls)),
]
