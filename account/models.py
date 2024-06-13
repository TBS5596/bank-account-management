from django.db import models
from django.contrib.auth.models import User
import random

class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="account")
    account_no = models.CharField(max_length=13, unique=True)
    branch_name = models.CharField(max_length=50, default="Main")
    branch_code = models.CharField(max_length=50, default="001")
    card_no = models.CharField(max_length=16, unique=True)
    card_expiry_date = models.DateField()
    pin = models.CharField(max_length=4)
    otp = models.CharField(max_length=6, default="000000")
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.account_no} - {self.balance}"

    def save(self, *args, **kwargs):
        if self.pin is None:
            self.pin = str(random.randint(1000, 9999))
        super().save(*args, **kwargs)