from django.shortcuts import render, redirect
from datetime import datetime
from django.contrib.auth import authenticate
from django.contrib.auth import logout as logout_function, login as login_function
from django.contrib.auth.decorators import login_required
from account.models import Account
from django.contrib import messages

def index(request):
    if request.user.is_authenticated == True:
        return redirect('account:index')
    return redirect('base:login')

def login(request):
    if request.method == "POST":
        card_no = request.POST.get('card_no')
        pin = request.POST.get('pin')

        account = Account.objects.filter(card_no=card_no, pin=pin).first()
        if account is None:
            messages.error(request, 'Invalid card number or pin!')
            return redirect('base:index')

        if datetime.now().date() > account.card_expiry_date:
            messages.error(request, 'This card has expired, please contact the bank for a replacement')
            return redirect('base:index')

        user = authenticate(username=account.user.username, password=account.user.password)
        if user is not None:
            login_function(request, user)
            return redirect('account:index')
        else:
            messages.error(request, 'Technical Error!')
            return redirect('base:index')
    else:
        if request.user.is_authenticated == True:
            return redirect('account:index')
            
        return render(request, 'base/login.html', {})

def login_app(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            login_function(request, user)
            return redirect('account:index')
        else:
            messages.error(request, 'Technical Error!')
            return redirect('base:index')
    else:
        if request.user.is_authenticated == True:
            return redirect('account:index')

        return render(request, 'base/login_app.html', {})


@login_required
def logout(request):
    logout_function(request)
    return redirect('base:index')