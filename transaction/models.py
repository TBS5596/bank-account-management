from django.db import models
from account.models import Account
from django.contrib.auth.models import User

class Transactions(models.Model):
    TRANSACTION_TYPE_CHOICES = (
        ('deposit', 'Deposit'),
        ('withdraw', 'Withdraw'),
        ('transfer', 'Transfer'),
    )

    TRANSACTION_STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('failed', 'Failed'),
    )

    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="transaction")
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE_CHOICES)
    transaction_status = models.CharField(max_length=10, choices=TRANSACTION_STATUS_CHOICES, default='pending')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="transaction_sender")
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="transaction_recipient")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.account.user.username} - {self.amount} - {self.created_at}"