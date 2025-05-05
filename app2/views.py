from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader

from .forms import UserProfileForm

# Create your views here.

def index_(request):
    return render(request,'home.html')


# def index(request):
#     template= loader.get_template('home.html')
#     return HttpResponse(template.render())

def user_profile(request):
    if request.method =='POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success')
    else:
        form = UserProfileForm()
    
    return render(request,'havenwatch/user_profile.html',{'form': form})

def success(request):
    return render(request,'success.html')