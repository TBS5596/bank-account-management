from django.urls import path
from . import views

app_name = "base"

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('login/app/', views.login_app, name='login-app'),
    path('logout/', views.logout, name='logout'),
]