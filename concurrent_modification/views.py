from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from django.utils import timezone
from .models import DebitCards, Transactions, Users, PersonalDetails, Addresses, Loans, Accounts, Admins, BankBranches, Employees, Overdrafts
from django.db.models import Q

class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')
    
    def post(self, request):
         # Extract all fields from the request form
        username = request.POST.get('username')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone_num = request.POST.get('phone_num')
        phone_area = request.POST.get('phone_area')
        street = request.POST.get('street')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip')

        # Check for required fields
        if not all([username, password, first_name, last_name, email, phone_num, phone_area, street, city, state, zip_code]):
            messages.error(request, "All fields are required.")
            return render(request, 'register.html')
        
        # Check for existing username
        if Users.objects.filter(username=username).exists():
            messages.error(request, "Username is already taken.")
            return render(request, 'register.html')

        # Check for existing email or phone number in personal details
        if PersonalDetails.objects.filter(Q(email=email) | Q(phone_num=phone_num)).exists():
            messages.error(request, "Email or phone number is already registered.")
            return render(request, 'register.html')

        # Create user
        try:
            # Add to the Users table
            user = Users.objects.create(
                username=username,
                pwd=password,
                created_at=timezone.now()
            )
            # Add to the PersonalDetails table
            personal = PersonalDetails.objects.create(
                details_username=user,
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone_num=phone_num,
                phone_area=phone_area
            )
            # Add to the Addresses table
            address = Addresses.objects.create(
                address_username=personal,
                address_street=street,
                addr_city=city,
                addr_state=state,
                addr_zip=zip_code
            )

            messages.success(request, "Account created successfully. Please log in.")
            return redirect('signin')

        except Exception as e:
            messages.error(request, f"Error creating account: {e}")
            return render(request, 'register.html')


class SigninView(View):
    def get(self, request):
        
        # Used to debug session data, prints out all info in the session
        #print("SESSION DATA:")
        #for key, value in request.session.items():
        #    print(f"{key}: {value}")

        request.session.flush()  # Clear all session data
        return render(request, 'signin.html')
    
    def post(self, request):
        # Get the username and password
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            # Get user from MySQL database
            user = Users.objects.get(username=username, pwd=password)
            request.session['user_id'] = user.user_id
            request.session['username'] = user.username
            personal = PersonalDetails.objects.get(details_username=user.username)
            print("Found personal details:", personal.first_name)
            request.session['first_name'] = personal.first_name

            if Admins.objects.filter(user=user).exists():
                return redirect('admin_home')

            else:
                return redirect('home')

        except Users.DoesNotExist:
            # The username or password are incorrect
            messages.error(request, "Invalid username or password. Please try again.\n")
            return render(request, 'signin.html')


class HomeView(View):
    def get(self, request):
        username = request.session.get('username')
        name = request.session.get('first_name')
        return render(request, 'homepage.html', {"username": username, "name": name})
    
class AccountView(View):
    def get(self, request):
        name = request.session.get('first_name')
        user_id = request.session.get('user_id')
        user = Users.objects.get(user_id=user_id)
        account = Accounts.objects.filter(user=user).first()
        return render(request, 'accounts.html', {'user': name, 'account' : account})

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
    
class DebitView(View):
    def get(self, request):
        user_id = request.session.get('user_id')
        if not user_id:
            return redirect('signin')

        try:
            account = Accounts.objects.get(user_id=user_id)
            last_txn = Transactions.objects.filter(acct=account).order_by('-trans_date', '-trans_time').first()
        except (Accounts.DoesNotExist, DebitCards.DoesNotExist):
            return render(request, 'debit.html', {'debit': None, 'user': request.session.get('username')})

        context = {
            'user': request.session.get('username'),
            'debit': {
                'balance': account.balance,
                'last_transaction': last_txn.trans_amt if last_txn else None,
                'connected_account': account.acct_id,
                'overdraft_protection': True,
                'is_active': bool(account.is_active),
            }
        }
        return render(request, 'debit.html', context)
    
class AdminView(View):
    def get(self, request):
        username = request.session.get('username')
        name = request.session.get('first_name')
        return render(request, 'admin_home.html', {"username": username, "name": name})
    
class BankBranchesView(View):
    def get(self, request):
        branches = BankBranches.objects.all()
        return render(request,'bank_branches.html', {'branches': branches})
    
class EmployeesView(View):
    def get(self, request):
        employees = Employees.objects.all()
        return render(request,'employees.html', {'employees': employees})

class OverdraftsView(View):
    def get(self, request):
        user_id = request.session.get('user_id')
        if not user_id:
            return redirect('signin')

        try:
            # Get the user's account(s)
            accounts = Accounts.objects.filter(user_id=user_id)

            if not accounts.exists():
                return render(request, 'overdrafts.html', {'overdrafts': [], 'user': request.session.get('username')})

            # Get all transactions for the user's accounts
            transactions = Transactions.objects.filter(acct__in=accounts)

            # Get all overdrafts linked to those transactions
            overdrafts = Overdrafts.objects.filter(overdraft_transaction__in=transactions)

        except Exception as e:
            print(e)
            return render(request, 'overdrafts.html', {'overdrafts': [], 'user': request.session.get('username')})

        context = {
            'user': request.session.get('username'),
            'overdrafts': overdrafts,
        }
        return render(request, 'overdrafts.html', context)
    
class PersonalInfoView(View):
    def get(self, request):
        user_id = request.session.get('user_id')

        if not user_id:
            return redirect('signin')

        try:
            user = Users.objects.get(user_id=user_id)
            personal = PersonalDetails.objects.get(details_username=user.username)
            address = Addresses.objects.get(address_username=personal)

        except (Users.DoesNotExist, PersonalDetails.DoesNotExist, Addresses.DoesNotExist):
            return render(request, 'personal_info.html', {'user_details': None})

        context = {
            'user': request.session.get('username'),
            'user_details': {
                'first_name': personal.first_name,
                'last_name': personal.last_name,
                'email': personal.email,
                'phone_area': personal.phone_area,
                'phone_num': personal.phone_num,
                'street': address.address_street,
                'city': address.addr_city,
                'state': address.addr_state,
                'zip_code': address.addr_zip,
            }
        }
        return render(request, 'personal_info.html', context)

class EditPersonalInfoView(View):
    def get(self, request):
        user_id = request.session.get('user_id')

        if not user_id:
            return redirect('signin')

        try:
            user = Users.objects.get(user_id=user_id)
            personal = PersonalDetails.objects.get(details_username=user.username)
            address = Addresses.objects.get(address_username=personal)

        except (Users.DoesNotExist, PersonalDetails.DoesNotExist, Addresses.DoesNotExist):
            return redirect('personal_info')

        context = {
            'user_details': {
                'first_name': personal.first_name,
                'last_name': personal.last_name,
                'email': personal.email,
                'phone_area': personal.phone_area,
                'phone_num': personal.phone_num,
                'street': address.address_street,
                'city': address.addr_city,
                'state': address.addr_state,
                'zip_code': address.addr_zip,
            }
        }
        return render(request, 'personal_info_edit.html', context)

    def post(self, request):
        user_id = request.session.get('user_id')

        if not user_id:
            return redirect('signin')

        try:
            user = Users.objects.get(user_id=user_id)
            personal = PersonalDetails.objects.get(details_username=user.username)
            address = Addresses.objects.get(address_username=personal)

        except (Users.DoesNotExist, PersonalDetails.DoesNotExist, Addresses.DoesNotExist):
            return redirect('personal_info')

        # Get form data
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        phone_area = request.POST['phone_area']
        phone_num = request.POST['phone_num']
        street = request.POST['street']
        city = request.POST['city']
        state = request.POST['state']
        zip_code = request.POST['zip_code']

        # Check if the email, or phone number is taken by another user
        if PersonalDetails.objects.filter(email=email).exclude(details_username=user.username).exists():
            messages.error(request, 'This email is already associated with another account.')
            return redirect('personal_info_edit')
        
        if PersonalDetails.objects.filter(phone_area=phone_area, phone_num=phone_num).exclude(details_username=user.username).exists():
            messages.error(request, 'This phone number is already in use.')
            return redirect('personal_info_edit')

        # Update the user details
        personal.first_name = first_name
        personal.last_name = last_name
        personal.email = email
        personal.phone_area = phone_area
        personal.phone_num = phone_num
        address.address_street = street
        address.addr_city = city
        address.addr_state = state
        address.addr_zip = zip_code

        personal.save()
        address.save()

        messages.success(request, 'Your details have been updated successfully.')
        return redirect('personal_info')
    
class ReactivateDebitView(View):
    def post(self, request):
        user_id = request.session.get('user_id')
        if not user_id: return redirect('signin')
        try:
            account = Accounts.objects.get(user_id=user_id)
            account.is_active = 1
            account.save()
            messages.success(request, "Debit card reactivated successfully.")
        except Accounts.DoesNotExist:
            messages.error(request, "Account not found.")     
        return redirect('debit')


class CloseDebitView(View):
    def post(self, request):
        user_id = request.session.get('user_id')
        if not user_id: return redirect('signin')
        try:
            account = Accounts.objects.get(user_id=user_id)
            account.is_active = 0
            account.save()
            messages.success(request, "Debit card closed successfully.")
        except Accounts.DoesNotExist:
            messages.error(request, "Account not found.")
        return redirect('debit')

class TransactionsView(View):
    def get(self, request):
        transactions = Transactions.objects.all()
        return render(request, 'transactions.html', {'transactions': transactions})

    def post(self, request):
        user_id = request.session.get('user_id')
        if not user_id: return redirect('signin')

        try:
            account = Accounts.objects.get(user_id=user_id)
        except Accounts.DoesNotExist:
            messages.error(request, "No account found.")
            return redirect('transactions')

        trans_type = request.POST.get('trans_type')
        trans_amount = request.POST.get('trans_amount')
        trans_note = request.POST.get('trans_note')

        if not all([trans_type, trans_amount]):
            messages.error(request, "Transaction type and amount are required.")
            return redirect('transactions')

        try:
            Transactions.objects.create(
                acct=account,
                trans_type=trans_type,
                trans_amt=trans_amount,
                trans_note=trans_note,
                trans_date=timezone.now().date(),
                trans_time=timezone.now().date()
            )
            messages.success(request, "Transaction created successfully.")
        except Exception as e:
            messages.error(request, f"Failed to create transaction: {e}")

        return redirect('transactions')
