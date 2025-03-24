from rest_framework.routers import DefaultRouter
from django.urls import path, include
from finance.views import TransactionViewSet, BudgetViewSet, SummaryView

router = DefaultRouter()
router.register(r"transaction", TransactionViewSet, basename="transactions")
router.register(r"budget", BudgetViewSet, basename="budget")

urlpatterns = [
    path("", include(router.urls)),
    path("summary/", SummaryView.as_view(), name="summary"),
]
