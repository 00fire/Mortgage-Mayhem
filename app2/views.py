from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
# Create your views here.
from .forms import PropertyForm
from app2.models import Properties

from django.contrib import messages
from .forms import SignUpForm, ProfileForm, ProfileEditForm


from .forms import PurchaseOfferForm
from app2.models import UserProfile,PurchaseOffer
from app2.forms import UserProfileForm
from .decorators import seller_required
from .decorators import buyer_required





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
    # -- 1) Profile edit form --
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile_info')
    else:
        form = UserProfileForm(instance=profile)

    # 2 Seller dashboard bits
    # All properties this user has listed
    my_listings = Properties.objects.filter(seller=request.user)

    # All offers other people have made against my listings
    incoming_offers = PurchaseOffer.objects.filter(
        property__seller=request.user,
        status='pending'
    ).order_by('-created_at')

    # -- 3) Buyer dashboard bits --
    # All offers I’ve made
    my_offers = PurchaseOffer.objects.filter(buyer=request.user)

    # All properties I’ve successfully purchased (accepted offers)
    purchased_properties = Properties.objects.filter(
        offers__buyer=request.user,
        offers__status='accepted'
    ).distinct()

    return render(request, 'profile_info.html', {
        'form': form,
        'my_listings': my_listings,
        'incoming_offers': incoming_offers,
        'my_offers': my_offers,
        'purchased_properties': purchased_properties,
    })





@login_required
def add_property(request):
    if request.method=='POST':
        form=PropertyForm(request.POST,request.FILES)
        if form.is_valid():
            prop=form.save(commit=False)
            prop.seller=request.user
            prop.save()
            return redirect('homepage')
        else:
            form=PropertyForm()
        return render(request, "add_property.html",{"form":form})

@buyer_required
def make_offer(request, property_id):
    # 1) fetch the property if it’s still unsold
    prop = get_object_or_404(
        Properties,
        pk=property_id,
        property_sold_status=False
    )

    # 2) look up any existing offer (but do NOT create one yet)
    existing = PurchaseOffer.objects.filter(
        property=prop,
        buyer=request.user
    ).first()

    if request.method == "POST":
        # 3a) bind POST data to a form — reusing existing instance if there is one
        form = PurchaseOfferForm(request.POST, instance=existing)
        if form.is_valid():
            offer = form.save(commit=False)
            offer.property = prop
            offer.buyer   = request.user
            offer.status  = "pending"
            offer.save()
            messages.success(request, "Your offer has been submitted.")
            return redirect("property_detail", id=property_id)
    else:
        # 3b) just display the empty (or pre-filled) form
        form = PurchaseOfferForm(instance=existing)

    return render(request, "offer_form.html", {
        "form": form,
        "property": prop,
    })

@login_required
def seller_dashboard(request):
    incoming=PurchaseOffer.objects.filter(property__seller=request.user).order_by("-created_at")
    return render(request,"seller_dashboard.html",{"incoming_offers":incoming,})










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