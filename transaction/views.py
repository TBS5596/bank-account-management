from django.shortcuts import render, redirect
from . models import Transactions, Account
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import random

@login_required
def index(request):
    transactions = Transactions.objects.filter(Q(account=request.user.account) | Q(recipient=request.user.account) | Q(sender=request.user.account))
    return render(request, 'transaction/index.html', {'transactions': transactions})

@login_required
def transfer(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        recipient = request.POST.get('recipient')

        if Account.objects.filter(account_no=recipient).exists():
            recipient = Account.objects.get(account_no=recipient)
        else:
            messages.error(request, 'Recipient account not found!')
            return redirect('transaction:transfer')

        account = Account.objects.get(user=request.user)
        if account.balance < float(amount):
            messages.error(request, 'Insufficient balance!')
            return redirect('transaction:transfer')

        sender_transaction = Transactions.objects.create(account=account, amount=amount, transaction_type='transfer', recipient=recipient.user, sender=request.user, transaction_status='pending')
        sender_transaction.save()

        account.balance =  float(account.balance) - float(amount)
        account.save()

        messages.success(request, "Transfer Requested!")
        return redirect('transaction:confirm-transfer', transfer_id=sender_transaction.id)
    else:
        return render(request, 'transaction/transfer.html', {})

@login_required
def confirm_transfer(request, transfer_id):
    try:
        transaction = Transactions.objects.get(id=transfer_id)
    except Transactions.DoesNotExist:
        messages.error(request, "Something went wrong! Transaction was not found!")
        return redirect('account:index')

    if request.method == "POST":
        otp = request.POST.get('otp')

        if transaction.account.otp != otp:
            transaction.transaction_status = "failed"
            transaction.save()

            transaction.account.balance = float(transaction.account.balance) + float(transaction.amount)
            transaction.account.save()

            messages.error(request, "Invalid OTP!")
            return redirect('account:index')
        else:
            transaction.transaction_status = "success"
            transaction.save()

            recipient_account = Account.objects.get(user=transaction.recepient)
            recipient_account.balance = float(recipient_account.balance) + float(transaction.amount)
            recipient_account.save()

            messages.success(request, "Transfer request made successfully!")
            return redirect('account:index')
    
    else:
        otp = random.randint(10000, 99999)
        transaction.account.otp = otp
        transaction.account.save()
        
        return render(request, "transaction/confirm_transfer.html", {'transaction': transaction})

@login_required
def withdraw(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')

        account = Account.objects.get(user=request.user)
        if account.balance < float(amount):
            messages.error(request, 'Insufficient balance!')
            return redirect('transaction:withdraw')

        transaction = Transactions.objects.create(account=account, amount=amount, transaction_type='withdraw', transaction_status='success')
        transaction.save()

        account.balance = float(account.balance) - float(amount)
        account.save()

        messages.success(request, 'Withdrawal successful!')
        return redirect('account:index')
    else:
        return render(request, 'transaction/withdraw.html', {})

@login_required
def deposit(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')

        account = Account.objects.get(user=request.user)

        transaction = Transactions.objects.create(account=account, amount=amount, transaction_type='deposit', transaction_status='success')
        transaction.save()

        account.balance = float(account.balance) + float(amount)
        account.save()

        messages.success(request, 'Deposit successful!')
        return redirect('account:index')
    else:
        return render(request, 'transaction/deposit.html', {})