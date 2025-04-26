"""
URL configuration for concurrent_modification project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import DebitView, SigninView, HomeView, RegisterView, LoansView, AccountView, AdminView, BankBranchesView, EmployeesView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', SigninView.as_view(), name='signin'),
    path('home/', HomeView.as_view(), name='home'),
    path('register/', RegisterView.as_view(), name='register'),
    path('loans/', LoansView.as_view(), name='loans'),
    path('accounts/', AccountView.as_view(), name='accounts'),
    path('debit/', DebitView.as_view(), name="debit"),
    path('admin_home', AdminView.as_view(), name='admin_home'),
    path('bank_branches/', BankBranchesView.as_view(), name='bank_branches'),
    path('employees/', EmployeesView.as_view(), name='employees')
]


