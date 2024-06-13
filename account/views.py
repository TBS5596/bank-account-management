from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Account
from django.db.models import Q
from transaction.models import Transactions

def rollback_transactions(request):
    transactions = Transactions.objects.filter(transaction_status="pending", sender=request.user)
    for transaction in transactions:
        transaction.account.balance = transaction.account.balance + transaction.amount
        transaction.transaction_status = "failed"
        transaction.save()

@login_required
def index(request):
    rollback_transactions()
    account = Account.objects.get(user=request.user)
    transactions = Transactions.objects.filter(Q(account=request.user.account) | Q(recipient=request.user) | Q(sender=request.user))
    return render(request, 'account/index.html', {'account': account, 'transactions': transactions})