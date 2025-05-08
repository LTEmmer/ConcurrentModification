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
from .views import DebitView, SigninView, HomeView, RegisterView, LoansView, AccountView, AdminView, BankBranchesView, EmployeesView, OverdraftsView, PersonalInfoView, EditPersonalInfoView, ReactivateDebitView, CloseDebitView, TransactionsView, AdminHelpView, AdminUsersView, HelpView, DeleteTicketView

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
    path('employees/', EmployeesView.as_view(), name='employees'),
    path('personal_info/', PersonalInfoView.as_view(), name='personal_info'),
    path('overdrafts/', OverdraftsView.as_view(), name='overdrafts'),
    path('personal_info_edit/', EditPersonalInfoView.as_view(), name='personal_info_edit'),
    path('debit/reactivate/', ReactivateDebitView.as_view(), name='debit_reactivate'),
    path('debit/close/', CloseDebitView.as_view(), name='debit_close'),
    path('transactions/', TransactionsView.as_view(), name='transactions'),
    path('admin_help/', AdminHelpView.as_view(), name='admin_help'),
    path('admin_help/delete/<int:ticket_id>/', AdminHelpView.as_view(), name='admin_help'),
    path('admin_users/', AdminUsersView.as_view(), name='admin_users'),
    path('transactions/', TransactionsView.as_view(), name='transactions'),
    path('help/', HelpView.as_view(), name='help'),
    path('help/submit/', HelpView.as_view(), name='submit_ticket'),
    path('help/delete/<int:ticket_id>/', DeleteTicketView.as_view(), name='delete_ticket'),
]


