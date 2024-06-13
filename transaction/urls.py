from django.urls import path
from . import views

app_name = 'transaction'

urlpatterns = [
    path('', views.index, name='index'),
    path('withdraw/', views.withdraw, name='withdraw'),
    path('deposit/', views.deposit, name='deposit'),
    path('transfer/', views.transfer, name='transfer'),
    path('transfer/<int:transfer_id>/', views.confirm_transfer, name='confirm-transfer'),
]