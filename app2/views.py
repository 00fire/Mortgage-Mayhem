from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login,authenticate
from app2.forms import UserPForm

# Create your views here.

def index_(request):
    return render(request,'home.html')

def register(response):
    form= UserCreationForm()
    return render(response, "register/register.html",{"form":form})

def user_profile(request):
    if request.method == 'POST':
        form = UserPForm(request.POST)  # Initialize form with POST data
        if form.is_valid():
            form.save()  # Save the form data to the database
            print("FROM IS VALID")
            print("Request method: ", request.method)
            print("form data: ", request.POST)
            return redirect('success')  # Redirect after saving
        else:
            print(form.errors)  # Print form validation errors to the console
            print("Request method: ", request.method)
            print("form data: ", request.POST)
    else:
        form = UserPForm()  # Initialize an empty form for GET request

    return render(request, 'home.html', {'form': form})  # Pass form to template









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

def success(request):
    return render(request,'success.html')