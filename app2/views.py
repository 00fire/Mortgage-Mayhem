from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate

from app2.models import Properties
from django.db.models import Q

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
# Create your views here.
from .forms import PropertyForm
from app2.models import Properties

from django.contrib import messages
from .forms import SignUpForm, ProfileForm, ProfileEditForm



from app2.models import UserProfile
from app2.forms import UserProfileForm


def root_redirect(request):
    return redirect("login")
@login_required#this renders the homepage
def homepage(request):
    properties=Properties.objects.all()
    return render(request, 'homepage.html',{'properties': properties})

#this renders the profile info html
def profile_info(request):
    return render(request,'profile_info.html')

def buyer_offer(request):
    return render(request,'buyer_offer.html')
#renders property detail page
def property_detail(request):
    return render(request, 'property_detail.html')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('homepage')
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})

def index_(request):
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to login if not authenticated
    return render(request, 'login.html')

# def register(request):
#     form = UserCreationForm()
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('login')  # After registration, go to login page
#     return render(request, "register/register.html", {"form": form})





# The @login_required decorator ensures that the user must be logged in to access this view


#@login_required
# def user_profile(request):
#     if request.method == 'POST':
#         form = UserPForm(request.POST)  # Initialize form with POST data
#         if form.is_valid():
#             username=form.cleaned_data.get('username')

#             if User.objects.filter(username=username).exists():
#                 form.add_error('username','this username is already taken.')
#             else:
#                 form.save()  # Save the form data to the database
#                 print("FORM IS VALID")
#                 print("Request method: ", request.method)
#                 print("Form data: ", request.POST)
#             return redirect('success')  # Redirect after saving to a success page
#         else:
#             print(form.errors)  # Print form validation errors to the console
#             print("Request method: ", request.method)
#             print("Form data: ", request.POST)
#     else:
#         form = UserPForm()  # Initialize an empty form for GET request

#     return render(request, 'home.html', {'form': form})  # Pass form to template

@login_required
def edit_profile(request):
    form = ProfileEditForm(request.POST or None,
                           request.FILES or None,
                           instance=request.user.profile)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("profile_info")

    return render(request, "profile/edit_profile.html", {"form": form})

def success(request):
    return render(request, 'success.html')  # Display success message


def add_property(request):
    if request.method=='POST':
        form=PropertyForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('homepage')
        else:
            form=PropertyForm
    return render(request,'add_property.html',{'form':form})


def property_detail(request, id):
    property=get_object_or_404(Properties, id=id)
    return render(request, 'property_detail.html', {'property': property})


def login_view(request):
    login_form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST" and login_form.is_valid():
        login(request, login_form.get_user())
        return redirect("homepage")

    return render(request, "login.html", {"login_form": login_form})

def signup_view(request):
    if request.method == "POST":
        user_form    = SignUpForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            # 1) create the user
            user = user_form.save(commit=False)
            user.is_active = True
            user.save()

            # 2) create / attach profile
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            # 3) log them straight in
            login(request, user)
            messages.success(request, "Welcome, your account was created.")
            return redirect("homepage")               # <- url‑name for /home/
    else:
        user_form    = SignUpForm()
        profile_form = ProfileForm()

    return render(
        request,
        "signup.html",                               # template you showed
        {"user_form": user_form, "profile_form": profile_form},
    )

@login_required
def profile_info(request):
    # Get the current user's profile or create a new one if it doesn't exist
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile_info')  # Redirect to the same profile page after saving
    else:
        form = UserProfileForm(instance=profile)
    
    return render(request, 'profile_info.html', {'form': form})


def search_properties(request):
    """
    View function to handle property search queries.

    Allows users to search for properties based on partial matches in
    the street, city, or country fields of the Properties model.

    Accepts:
        - GET parameter 'q': the search query string

    Returns:
        - Rendered HTML page ('search_page.html') with a context variable
          'properties' containing the filtered queryset.
    """
    
    # Retrieve the value of the search query from the GET request
    query = request.GET.get('q')
    city = request.GET.getlist('city')  # multiple cities via checkbox
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    rooms = request.GET.getlist('rooms')  # filter by room count

    # Get all properties initially
    properties = Properties.objects.all()

    if query:
         # Q objects allow combining filters using | (OR), & (AND), and ~ (NOT)
        # __icontains performs a case-insensitive partial string match
        properties = properties.filter(
            Q(property_street__icontains=query) |
            Q(property_city__icontains=query) |
            Q(property_country__icontains=query)
        )

    if city:
        properties = properties.filter(property_city__in=city)

    if rooms:
        properties = properties.filter(property_rooms__in=rooms)

    if min_price:
        properties = properties.filter(property_price__gte=min_price)
    if max_price:
        properties = properties.filter(property_price__lte=max_price)

    all_cities = Properties.objects.values_list('property_city', flat=True).distinct()
    all_rooms = Properties.objects.values_list('property_rooms', flat=True).distinct()

    # Render the search results in the 'search_page.html' template
    return render(request, 'search_page.html', {
        'properties': properties,
        'all_cities': all_cities,
        'all_rooms': all_rooms,
    })



































#@login_required
# def user_profile(request):
#     if request.method == 'POST':
#         form = UserPForm(request.POST)  # Initialize form with POST data
#         if form.is_valid():
#             form.save()  # Save the form data to the database
#             print("FORM IS VALID")
#             print("Request method: ", request.method)
#             print("Form data: ", request.POST)
#             return redirect('success')  # Redirect after saving to a success page
#         else:
#             print(form.errors)  # Print form validation errors to the console
#             print("Request method: ", request.method)
#             print("Form data: ", request.POST)
#     else:
#         form = UserPForm()  # Initialize an empty form for GET request

#     return render(request, 'home.html', {'form': form})  # Pass form to template

# Success page after creating a user profile



# def login_view(request):
#     if request.method=='POST':
#         form= AuthenticationForm(request, data=request.POST)
#         if form.is_valid():
#             username=form.cleanedÖdate.get('username')
#             password=form.cleanedÖdate.get('password')
#             user=authenticate(username=username,password=password)
#             if user is not None:
#                 login(request,user)
#                 return redirect('user_profile')
#             else:
#                 form.add_error(None,'Invalid username or password')
#     else:
#         form=AuthenticationForm()

#     return render(request,'login.html',{'form':form})
# def index_(request):
#     return render(request,'home.html')

# def register(response):
#     form= UserCreationForm()
#     return render(response, "register/register.html",{"form":form})
# @login_required
# def user_profile(request):
#     if request.method == 'POST':
#         form = UserPForm(request.POST)  # Initialize form with POST data
#         if form.is_valid():
#             form.save()  # Save the form data to the database
#             print("FROM IS VALID")
#             print("Request method: ", request.method)
#             print("form data: ", request.POST)
#             return redirect('login')  # Redirect after saving
#         else:
#             print(form.errors)  # Print form validation errors to the console
#             print("Request method: ", request.method)
#             print("form data: ", request.POST)
#     else:
#         form = UserPForm()  # Initialize an empty form for GET request

#     return render(request, 'home.html', {'form': form})  # Pass form to template









# def index(request):
#     template= loader.get_template('home.html')
#     return HttpResponse(template.render())

# def user_profile(request):
#     if request.method == 'POST':
#         form=UserPForm(request.POST)
#         if form.is_valid():
#             form.save()
#             #ok
#             #i've cum
#             return redirect('app2:success')
#     form = UserPForm()
#     return render(request, 'home.html', {'message': 'Profile created successfully!'})

# def user_profile(request):
#     if request.method == 'POST':
#         # Get the form data
#         username = request.POST.get("username")
#         password = request.POST.get("password")
#         print("Post was a successssss!")

#         # Create an instance of the form with the POST data
#         user_form = UserPForm(request.POST)

#         # Validate the form
#         if user_form.is_valid():
#             # Save the form data to the database
#             user_form.save()
#             print(f'User {username} saved successfully!')

#             print("Data saved successfully!")

#             # Optionally, redirect to a success page or render a success template
#             return render(request, 'home.html', {'message': 'Profile created successfully!'})

#         else:
#             # If the form is invalid, print errors
#             print("Form errors:", user_form.errors)
#             return render(request, 'home.html', {'form': user_form})

#     # If the request is not POST, render the form as usual
#     else:
#         user_form = UserPForm()

#     return render(request, 'home.html', {'form': user_form})

# # 
# def success(request):
#     return render(request,'success.html')