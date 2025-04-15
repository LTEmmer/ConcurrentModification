from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.views import View
from django.utils import timezone
from .models import Users, PersonalDetails, Addresses
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
            return redirect('home')

        except Users.DoesNotExist:
            # The username or password are incorrect
            messages.error(request, "Invalid username or password. Please try again.\n")
            return render(request, 'signin.html')


class HomeView(View):
    def get(self, request):
        username = request.session.get('username')
        print("GET username from session:", username)
        print(username)
        return render(request, 'homepage.html', {"username": username})
    
    # Probably don't need POST for homepage yet, uncomment when needed
    #def post(self, request):
    #    username = request.session.get('username')
    #    print("POST username from session:", username)
    #    return render(request, 'homepage.html', {"username": username})
