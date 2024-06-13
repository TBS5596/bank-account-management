from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from .models import Account

class CardNoPinBackend(BaseBackend):
    def authenticate(self, request, card_no=None, pin=None):
        try:
            account = Account.objects.get(card_no=card_no, pin=pin)
            return account.user
        except ObjectDoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
