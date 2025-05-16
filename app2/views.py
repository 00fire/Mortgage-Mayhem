# Django Core Imports
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden, HttpResponse
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Q
from .models import Properties, PropertyImage, FinalizedOffer, UserProfile, PurchaseOffer
from .forms import (PropertyForm, PropertyImageFormSet, SignUpForm, ProfileForm, ProfileEditForm,PurchaseOfferForm, UserProfileForm, ContactInfoForm, PaymentForm)
from .decorators import seller_required, buyer_required



def root_redirect(request):
    return redirect("login")


@login_required#this renders the homepage
def homepage(request):
    properties=Properties.objects.all()#this fetches all of the property listings
    return render(request, 'homepage.html',{'properties': properties})#adn here we pass them to the homepage

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
            password = form.cleaned_data.get('password')#this is all to handle logging in and to validate if the form is okay
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('homepage')#if everything works then we get routed to the homepage
            else:
                form.add_error(None, 'Invalid username or password')#else we get an error
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})

def index_(request):
    if not request.user.is_authenticated:
        return redirect('login')  #redirect to login if the user is not authenticated
    return render(request, 'login.html')



@login_required
def edit_profile(request):#here i initialize the form with post data nad files and bind them to the users current profile
    form = ProfileEditForm(request.POST or None,
                           request.FILES or None,
                           instance=request.user.profile)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("profile_info")#if the form is valid and submittted we get redirected to the users profile
    

    return render(request, "profile/edit_profile.html", {"form": form})

def success(request):
    return render(request, 'success.html')  # Display success message

@login_required

def property_detail(request, pk):
    prop = get_object_or_404(Properties, pk=pk)#we look up the property by primary key, return a 404 if it ain't there
    existing = None
    offer_form = None

    #only for buyers who can make an offer so that sellers can't
    if request.user.is_authenticated \
       and request.user.profile.role == "buyer" \
       and prop.seller != request.user \
       and not prop.property_sold_status:
        
        existing = prop.offers.filter(buyer=request.user).first()#here we check if there is already a buyer
        offer_form = PurchaseOfferForm(request.POST or None, instance=existing)

        if request.method=="POST" and offer_form.is_valid():
            off = offer_form.save(commit=False)
            off.property = prop
            off.buyer = request.user
            off.status = "pending"
            off.save()
            messages.success(request, "Your offer has been submitted.")###################CHECK THISS
            return redirect("property_detail", pk=prop.pk)#if everything is valid then the offer is saved and the buyer is redirected to the prop details page

    return render(request, "property_detail.html", {
        "property": prop,
        "offer_form": offer_form,
        "existing_offer": existing,
    })



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

        if user_form.is_valid() and profile_form.is_valid():#this is gonna ensure that of both forms are valid then a new user is activated and saved to the system
            
            user = user_form.save(commit=False)
            user.is_active = True#the user is activated
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.role = user_form.cleaned_data["role"]
            profile.save()
            login(request, user)#we do an auto login after the sign up, very cool i know :3
            messages.success(request, "Welcome, your account was created.")
            return redirect("homepage")

    else:
        user_form    = SignUpForm()
        profile_form = ProfileForm()#we also makel it so that they get a dedicated userprofile

    return render(request, "signup.html", {
        "user_form":    user_form,
        "profile_form": profile_form,
    })

@login_required
def profile_info(request):
    # profile form handling 
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    #if the user submitted any changes then they are saved
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()#we save them here
            return redirect('profile_info')
    else:
        form = UserProfileForm(instance=profile)

    #this is is just what we show on the seller side of things, invisible to the buyer
    if request.user.profile.role == 'seller':
        my_listings = Properties.objects.filter(
            seller=request.user,
            property_sold_status=False
        )
        incoming_offers = PurchaseOffer.objects.filter(
            property__seller=request.user,
            status='pending'
        ).order_by('-created_at')
        incoming_count = incoming_offers.count()
    else:
        my_listings = Properties.objects.none()
        incoming_offers = Properties.objects.none()
        incoming_count = 0

    #the buyer only sees this part, this is their dashboard
    my_offers = PurchaseOffer.objects.filter(buyer=request.user)
    for offer in my_offers:
        offer.finalized = FinalizedOffer.objects.filter(purchase_offer=offer).exists()
    #this is shown regardless of the role, just all the properties they own
    my_owned = Properties.objects.filter(owner=request.user)

    return render(request, 'profile_info.html', {
        'form':             form,
        'incoming_offers':  incoming_offers,
        'incoming_count':   incoming_count,
        'my_listings':      my_listings,
        'my_offers':        my_offers,
        'my_owned':         my_owned,
    })


















def homepage(request):
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

    #here we retreive filter inputs from the get parameters
    query = request.GET.get('q', '')
    postal_code = request.GET.get('postal_code', '')
    property_type = request.GET.get('property_type', '')
    street_name = request.GET.get('street_name', '')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    order_by = request.GET.get('order_by', '')
    #we start with all properties
    properties = Properties.objects.all()

    if query:
        properties = properties.filter(
            Q(property_street__icontains=query) |
            Q(property_city__icontains=query) |
            Q(property_country__icontains=query)
        )
    #this is to search by postal code
    if postal_code:
        properties = properties.filter(property_postal__iexact=postal_code)
    #this is to search by property type
    if property_type:
        properties = properties.filter(property_type__iexact=property_type)
    #this is to search by street name
    if street_name:
        properties = properties.filter(property_street__icontains=street_name)
    #this is to search by min price
    if min_price:
        properties = properties.filter(property_price__gte=min_price)
    #this is to search by max price
    if max_price:
        properties = properties.filter(property_price__lte=max_price)

    #by price
    if order_by == 'price':
        properties = properties.order_by('property_price')
    #by name
    elif order_by == 'name':
        properties = properties.order_by('property_street')
    #all possible quires
    context = {
        'properties': properties,
        'current_query': query,
        'postal_code': postal_code,
        'property_type': property_type,
        'street_name': street_name,
        'min_price': min_price,
        'max_price': max_price,
        'order_by': order_by,
    }

    return render(request, 'homepage.html', context)





############### buyer related
@buyer_required
def make_offer(request, property_id):
    
    prop = get_object_or_404(Properties,pk=property_id,property_sold_status=False)#here we fetch the property id but only if its available
    existing = PurchaseOffer.objects.filter(property=prop,buyer=request.user).first()

    if request.method == "POST":
        
        form = PurchaseOfferForm(request.POST, instance=existing)
        if form.is_valid():
            offer = form.save(commit=False)
            offer.property = prop
            offer.buyer   = request.user
            offer.status  = "pending"
            offer.save()
            messages.success(request, "Your offer has been submitted.")
            return redirect("property_detail", id=property_id)#just a standard saving form
    else:
        
        form = PurchaseOfferForm(instance=existing)

    return render(request, "offer_form.html", {
        "form": form,
        "property": prop,
    })













################ seller related




def seller_profile(request,user_id):
    seller=get_object_or_404(User,pk=user_id)#fetch the seller by their userid
    profile=seller.profile#get their profile
    listings=Properties.objects.filter(seller=seller,property_sold_status=False)

    return render(request,'seller_profile.html',{'seller':seller,'profile':profile,'listings':listings,})







@login_required
def incoming_offers(request):
    if request.user.profile.role !='seller':
        return HttpResponseForbidden()
    offers=PurchaseOffer.objects.filter(property__seller=request.user,status='pending').select_related('buyer','property')#this shows every pending offer
    return render(request,"seller_incoming_offers.html",{"offers":offers})






@login_required
def respond_offer(request, offer_id):
    offer = get_object_or_404(PurchaseOffer, pk=offer_id)#this gets the offer
    if request.user != offer.property.seller:
        return HttpResponseForbidden()

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'accept':
            #  mark the offer accepted
            offer.status = 'accepted'
            offer.save()#this makes sure the offer is saved if accepted

           #transfer ownership & mark sold
            # prop = offer.property
            # prop.property_sold_status = True
            # prop.owner = offer.buyer
            # prop.save()

            messages.success(request, f"Offer #{offer.id} accepted and ownership transferred.")
        else:
            offer.status = 'rejected'
            messages.info(request, f"Offer #{offer.id} rejected.")
            offer.save()#saved if rejected
            

        
        return redirect('seller_listings')

    
    return render(request, 'respond_offer.html', {'offer': offer})





@login_required
def seller_dashboard(request):
    incoming=PurchaseOffer.objects.filter(property__seller=request.user).order_by("-created_at")
    return render(request,"seller_dashboard.html",{"incoming_offers":incoming,})#this renders the seller dashboard


def seller_listings(request):
    if request.user.profile.role !='seller':
        return HttpResponseForbidden()
    my_listings=Properties.objects.filter(seller=request.user)#this is so taht only the sellers can access
    incoming=PurchaseOffer.objects.filter(property__seller=request.user,status='pending').order_by('-created_at')#this makes it so we see the pending offers
    return render(request,'seller_listings.html',{'listings':my_listings,'incoming_offers':incoming,})








@login_required#this is a standard adding form just shanghaied into working for adding property
def add_property(request):
    if request.user.profile.role != 'seller':
        return HttpResponseForbidden("Only sellers can list properties")
    
    if request.method == 'POST':
        prop_form = PropertyForm(request.POST, request.FILES)
        img_formset = PropertyImageFormSet(request.POST, request.FILES, queryset=PropertyImage.objects.none())

        if prop_form.is_valid() and img_formset.is_valid():
            prop = prop_form.save(commit=False)
            prop.seller = request.user
            prop.owner = request.user
            prop.save()

            images = img_formset.save(commit=False)
            for image in images:
                image.property = prop
                image.save()

            # Auto-set the first uploaded image as main if none was uploaded
            if not prop.property_image and images:
                prop.property_image = images[0].image
                prop.save()

            return redirect('profile_info')
    else:
        prop_form = PropertyForm()
        img_formset = PropertyImageFormSet(queryset=PropertyImage.objects.none())

    return render(request, "add_property.html", {
        "form": prop_form,
        "formset": img_formset,
    })



def contact_info(request, property_id):#this is for the first step of finalizing a purchase
    if request.method == 'POST':
        form = ContactInfoForm(request.POST)
        if form.is_valid():#standard if the form is valid
            print("POST received in contact_info")
            request.session['contact_info'] = form.cleaned_data
            return redirect('payment', property_id=property_id)
    else:
        form = ContactInfoForm(initial=request.session.get('contact_info', {}))

    return render(request, 'contact_info.html', {'form': form})



    
def payment(request,property_id):#this is the chose payment method and where we enter the card credentials
    if request.method=='POST':
        form=PaymentForm(request.POST)
        if form.is_valid():
            #here we save the payment info in the current session
            request.session['payment_info']=form.cleaned_data
            return redirect('review',property_id=property_id)
    else:
        #and here we can reload said info if we are returning
        form=PaymentForm(initial=request.session.get('payment_info',{}))
    return render(request,'payment.html',{'form':form})
#this is the final step in finalization
def review(request, property_id):
    contact_info = request.session.get('contact_info', {}).copy()
    payment_info = request.session.get('payment_info', {}).copy()
    property = get_object_or_404(Properties, pk=property_id)

    if 'payment_option' in payment_info:
        payment_info['pay_method'] = payment_info.pop('payment_option')

    if request.method == 'POST':
        
        offer = PurchaseOffer.objects.filter(
            buyer=request.user,
            property=property,
            status__iexact='accepted'
        ).first()#here we can validate taht an accepted offer exists before we finalize it

        if not offer:
            return HttpResponse("No matching accepted offer found", status=400)

        
        finalized = FinalizedOffer.objects.create(
            user=request.user,
            property=property,
            purchase_offer=offer,
            **contact_info,
            **payment_info
        )#here we save all the info to finalizedoffer table

        #the actual transfer ownership
        property.owner = request.user
        property.property_sold_status = True
        property.save()

        #clean up so that the info is correct
        request.session.pop('contact_info', None)
        request.session.pop('payment_info', None)

        return redirect('confirmation')

    return render(request, 'review.html', {
        'contact_info': contact_info,
        'payment_info': payment_info,
        'property': property
    })


#this is just a render to show a little confirmation message after a successful pruchase    
def confirmation(request):
    return render(request,'confirmation.html')


# ADMIN FEATURES

@login_required
def delete_property(request, property_id):
    prop = get_object_or_404(Properties, id=property_id)

    if request.user.profile.role != 'admin':
        messages.error(request, "You do not have permission to delete this property.")
    elif prop.property_sold_status:
        messages.warning(request, "This property has already been sold and cannot be deleted.")
    else:
        prop.delete()
        messages.success(request, "Property listing successfully deleted.")
        return redirect('homepage')

    return redirect('property_detail', pk=property_id)