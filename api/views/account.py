from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from account.models import Account
from api.serializers import AccountSerializer

def account_data(account):
    data = {
        "id": account.id,
        "account_no": account.account_no,
        "branch_name": account.branch_name,
        "branch_code": account.branch_code,
        "card_no": account.card_no,
        "card_expiry_date": account.card_expiry_date,
        "pin": account.pin,
        "otp": account.otp,
        "balance": account.balance,
        "created_at":account.created_at,
        "updated_at": account.updated_at,
        "user_id": account.user.id,
        "username": account.user.username,
        "first_name": account.user.first_name,
        "last_name": account.user.last_name,
        "email": account.user.email
    }
    return data

@api_view(['GET', 'PUT', 'DELETE'])
def account_by_id(request, id):
    try:
        account = Account.objects.get(id=id)
    except Account.DoesNotExist:
        return Response({"message":"Account with given ID does not exist"}, status=status.HTTP_200_OK)

    if request.method == "GET":
        serializer = AccountSerializer(account, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({"error":"Invalid Request"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    
@api_view(['GET'])
def account_by_no(request, no):
    try:
        account = Account.objects.get(account_no=no)
    except Account.DoesNotExist:
        return Response({"message":"Account with given number does not exist"}, status=status.HTTP_200_OK)
    
    if request.method == "GET":
        return Response(account_data(account), status=status.HTTP_200_OK)
    else:
        return Response({"error":"Invalid Request"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)