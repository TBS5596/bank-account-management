from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from django.db.models import Q
from account.models import Account
from transaction.models import Transactions

@api_view(['GET'])
def transactions_pie_by_account(request, id):
    try:
        account = Account.objects.get(id=id)
    except Account.DoesNotExist:
        return Response({"message":"Account with given ID does not exist"}, status=status.HTTP_200_OK)
    
    if request.method == "GET":
        transactions = Transactions.objects.filter(Q(account=account) | Q(recipient=account.user) | Q(sender=account.user))
        labels = ['withdraw', 'deposit', 'transfer']
        series = []

        for label in labels:
            count = transactions.filter(transaction_type=label).count()
            series.append(count)

        total = transactions.count()

        return Response({"series":series, "labels":labels, "total":total}, status=status.HTTP_200_OK)
    else:
        return Response({"error":"Invalid Request"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    
@api_view(['GET'])
def transactions_bar_by_account(request, id):
    try:
        account = Account.objects.get(id=id)
    except Account.DoesNotExist:
        return Response({"message":"Account with given ID does not exist"}, status=status.HTTP_200_OK)
    
    if request.method == "GET":
        transactions = Transactions.objects.filter(Q(account=account) | Q(recipient=account.user) | Q(sender=account.user))
        labels = ['withdraw', 'deposit', 'transfer']
        series = []

        for label in labels:
            count = transactions.filter(transaction_type=label).count()
            series.append(count)

        total = transactions.count()

        return Response({"series":series, "labels":labels, "total":total}, status=status.HTTP_200_OK)
    else:
        return Response({"error":"Invalid Request"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)