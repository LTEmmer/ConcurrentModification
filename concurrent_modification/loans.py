from django.shortcuts import render, redirect
from django.urls import path
from django.views import View
from .models import Loans

class LoansView(View):
    def get(self, request):
        # redirect if not signed in
        user_id = request.session.get('user_id')
        if not user_id:
            return redirect('signin')

        # pull this user’s loans
        loans = (
            Loans.objects
                 .filter(loan_account__user__user_id=user_id)
                 .order_by('-created_at')
        )
        return render(request, 'loans.html', {'loans': loans})

# expose this to your main URL conf:
loans_urlpatterns = [
    path('loans/', LoansView.as_view(), name='loans'),
]
