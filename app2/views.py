from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate
from app2.forms import UserPForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
# Create your views here.
from .forms import PropertyForm
from app2.models import Properties
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

def register(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # After registration, go to login page
    return render(request, "register/register.html", {"form": form})

# The @login_required decorator ensures that the user must be logged in to access this view


#@login_required
def user_profile(request):
    if request.method == 'POST':
        form = UserPForm(request.POST)  # Initialize form with POST data
        if form.is_valid():
            username=form.cleaned_data.get('username')

            if User.objects.filter(username=username).exists():
                form.add_error('username','this username is already taken.')
            else:
                form.save()  # Save the form data to the database
                print("FORM IS VALID")
                print("Request method: ", request.method)
                print("Form data: ", request.POST)
            return redirect('success')  # Redirect after saving to a success page
        else:
            print(form.errors)  # Print form validation errors to the console
            print("Request method: ", request.method)
            print("Form data: ", request.POST)
    else:
        form = UserPForm()  # Initialize an empty form for GET request

    return render(request, 'home.html', {'form': form})  # Pass form to template



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