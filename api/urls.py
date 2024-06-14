from django.urls import path
from api.views import account, transaction

urlpatterns = [
    path('accounts/id/<int:id>/', account.account_by_id),
    path('accounts/no/<int:no>/', account.account_by_no),

    path('transactions/stats/<int:id>/pie/', transaction.transactions_pie_by_account)
]