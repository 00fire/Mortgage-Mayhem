from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate

from app2.models import Properties
from django.db.models import Q
from django.shortcuts import render
from django.db.models import Q
from .models import Properties
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
# Create your views here.
from .forms import PropertyForm
from app2.models import Properties
from django.http import HttpResponseForbidden,HttpResponse
from django.contrib import messages
from .forms import SignUpForm, ProfileForm, ProfileEditForm


from .forms import PurchaseOfferForm
from app2.models import UserProfile,PurchaseOffer
from app2.forms import UserProfileForm
from .decorators import seller_required
from .decorators import buyer_required
from django.contrib import messages

from django.utils import timezone


from .forms import PropertyForm, PropertyImageFormSet
from .models import Properties, PropertyImage


from .forms import ContactInfoForm, PaymentForm
from .models import Properties, FinalizedOffer





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
from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden
@login_required

def property_detail(request, pk):
    prop = get_object_or_404(Properties, pk=pk)
    existing = None
    offer_form = None

    # only for buyers who can make an offer
    if request.user.is_authenticated \
       and request.user.profile.role == "buyer" \
       and prop.seller != request.user \
       and not prop.property_sold_status:

        existing = prop.offers.filter(buyer=request.user).first()
        offer_form = PurchaseOfferForm(request.POST or None, instance=existing)

        if request.method=="POST" and offer_form.is_valid():
            off = offer_form.save(commit=False)
            off.property = prop
            off.buyer = request.user
            off.status = "pending"
            off.save()
            messages.success(request, "Your offer has been submitted.")
            return redirect("property_detail", pk=prop.pk)

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

        if user_form.is_valid() and profile_form.is_valid():
            
            user = user_form.save(commit=False)
            user.is_active = True
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.role = user_form.cleaned_data["role"]
            profile.save()
            login(request, user)
            messages.success(request, "Welcome, your account was created.")
            return redirect("homepage")

    else:
        user_form    = SignUpForm()
        profile_form = ProfileForm()

    return render(request, "signup.html", {
        "user_form":    user_form,
        "profile_form": profile_form,
    })

@login_required
def profile_info(request):
    # — Profile form handling (unchanged) —
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile_info')
    else:
        form = UserProfileForm(instance=profile)

    # — Seller dashboard bits (only if role == 'seller') —
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

    # — Buyer dashboard bits —
    my_offers = PurchaseOffer.objects.filter(buyer=request.user)
    for offer in my_offers:
        offer.finalized = FinalizedOffer.objects.filter(purchase_offer=offer).exists()
    # — Everything I own (regardless of role) —
    my_owned = Properties.objects.filter(owner=request.user)

    return render(request, 'profile_info.html', {
        'form':             form,
        'incoming_offers':  incoming_offers,
        'incoming_count':   incoming_count,
        'my_listings':      my_listings,
        'my_offers':        my_offers,
        'my_owned':         my_owned,
    })















# def search_properties(request):
#     """
#     View function to handle property search queries.

#     Allows users to search for properties based on partial matches in
#     the street, city, or country fields of the Properties model.

#     Accepts:
#         - GET parameter 'q': the search query string

#     Returns:
#         - Rendered HTML page ('search_page.html') with a context variable
#           'properties' containing the filtered queryset.
#     """
    
#     # Retrieve the value of the search query from the GET request
#     query = request.GET.get('q')
#     city = request.GET.getlist('city')  # multiple cities via checkbox
#     min_price = request.GET.get('min_price')
#     max_price = request.GET.get('max_price')
#     rooms = request.GET.getlist('rooms')  # filter by room count

#     # Get all properties initially
#     properties = Properties.objects.all()

#     if query:
#          # Q objects allow combining filters using | (OR), & (AND), and ~ (NOT)
#         # __icontains performs a case-insensitive partial string match
#         properties = properties.filter(
#             Q(property_street__icontains=query) |
#             Q(property_city__icontains=query) |
#             Q(property_country__icontains=query)
#         )

#     if city:
#         properties = properties.filter(property_city__in=city)

#     if rooms:
#         properties = properties.filter(property_rooms__in=rooms)

#     if min_price:
#         properties = properties.filter(property_price__gte=min_price)
#     if max_price:
#         properties = properties.filter(property_price__lte=max_price)

#     all_cities = Properties.objects.values_list('property_city', flat=True).distinct()
#     all_rooms = Properties.objects.values_list('property_rooms', flat=True).distinct()

#     # Render the search results in the 'search_page.html' template
#     return render(request, 'homepage.html', {
#         'properties': properties,
#         'all_cities': all_cities,
#         'all_rooms': all_rooms,
#         'current_query': query,
#         'selected_cities': city,
#         'selected_rooms': rooms,
#         'min_price': min_price,
#         'max_price': max_price,
#     })



def homepage(request):
    query = request.GET.get('q', '')
    postal_code = request.GET.get('postal_code', '')
    property_type = request.GET.get('property_type', '')
    street_name = request.GET.get('street_name', '')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    order_by = request.GET.get('order_by', '')

    properties = Properties.objects.all()

    if query:
        properties = properties.filter(
            Q(property_street__icontains=query) |
            Q(property_city__icontains=query) |
            Q(property_country__icontains=query)
        )

    if postal_code:
        properties = properties.filter(property_postal__iexact=postal_code)

    if property_type:
        properties = properties.filter(property_type__iexact=property_type)

    if street_name:
        properties = properties.filter(property_street__icontains=street_name)

    if min_price:
        properties = properties.filter(property_price__gte=min_price)

    if max_price:
        properties = properties.filter(property_price__lte=max_price)

    
    if order_by == 'price':
        properties = properties.order_by('property_price')
    elif order_by == 'name':
        properties = properties.order_by('property_street')

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
    
    prop = get_object_or_404(Properties,pk=property_id,property_sold_status=False)
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
            return redirect("property_detail", id=property_id)
    else:
        # 3b) just display the empty (or pre-filled) form
        form = PurchaseOfferForm(instance=existing)

    return render(request, "offer_form.html", {
        "form": form,
        "property": prop,
    })













################ seller related




def seller_profile(request,user_id):
    seller=get_object_or_404(User,pk=user_id)
    profile=seller.profile
    listings=Properties.objects.filter(seller=seller,property_sold_status=False)

    return render(request,'seller_profile.html',{'seller':seller,'profile':profile,'listings':listings,})







@login_required
def incoming_offers(request):
    if request.user.profile.role !='seller':
        return HttpResponseForbidden()
    offers=PurchaseOffer.objects.filter(property__seller=request.user,status='pending').select_related('buyer','property')
    return render(request,"seller_incoming_offers.html",{"offers":offers})






@login_required
def respond_offer(request, offer_id):
    offer = get_object_or_404(PurchaseOffer, pk=offer_id)
    if request.user != offer.property.seller:
        return HttpResponseForbidden()

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'accept':
            #  mark the offer accepted
            offer.status = 'accepted'
            offer.save()

           #transfer ownership & mark sold
            # prop = offer.property
            # prop.property_sold_status = True
            # prop.owner = offer.buyer
            # prop.save()

            messages.success(request, f"Offer #{offer.id} accepted and ownership transferred.")
        else:
            offer.status = 'rejected'
            messages.info(request, f"Offer #{offer.id} rejected.")
            offer.save()
            

        # redirect back to _your_ profile dashboard
        return redirect('seller_listings')

    # GET: show the “accept / reject” form
    return render(request, 'respond_offer.html', {'offer': offer})





@login_required
def seller_dashboard(request):
    incoming=PurchaseOffer.objects.filter(property__seller=request.user).order_by("-created_at")
    return render(request,"seller_dashboard.html",{"incoming_offers":incoming,})


def seller_listings(request):
    if request.user.profile.role !='seller':
        return HttpResponseForbidden()
    my_listings=Properties.objects.filter(seller=request.user)
    incoming=PurchaseOffer.objects.filter(property__seller=request.user,status='pending').order_by('-created_at')
    return render(request,'seller_listings.html',{'listings':my_listings,'incoming_offers':incoming,})






@login_required
def add_property(request):
    if request.user.profile.role !='seller':
        return HttpResponseForbidden("Only sellers can list properties")
    
    if request.method=='POST':
        prop_form=PropertyForm(request.POST,request.FILES)
        img_formset=PropertyImageFormSet(request.POST,request.FILES,queryset=PropertyImage.objects.none())
        #form=PropertyForm(request.POST,request.FILES)
        
        if prop_form.is_valid() and img_formset.is_valid():
            prop=prop_form.save(commit=False)
            prop.seller=request.user
            prop.owner=request.user
            prop.save()
            images = img_formset.save(commit=False)
            for image in images:
                image.property = prop
                image.save()
            return redirect('profile_info')
    else:
            prop_form=PropertyForm()
            img_formset=PropertyImageFormSet(queryset=PropertyImage.objects.none())
    return render(request, "add_property.html",{"form":prop_form,'formset':img_formset,})


def contact_info(request, property_id):
    if request.method == 'POST':
        form = ContactInfoForm(request.POST)
        if form.is_valid():
            print("POST received in contact_info")
            request.session['contact_info'] = form.cleaned_data
            return redirect('payment', property_id=property_id)
    else:
        form = ContactInfoForm(initial=request.session.get('contact_info', {}))

    return render(request, 'contact_info.html', {'form': form})



    
def payment(request,property_id):
    if request.method=='POST':
        form=PaymentForm(request.POST)
        if form.is_valid():
            request.session['payment_info']=form.cleaned_data
            return redirect('review',property_id=property_id)
    else:
        form=PaymentForm(initial=request.session.get('payment_info',{}))
    return render(request,'payment.html',{'form':form})

def review(request, property_id):
    contact_info = request.session.get('contact_info', {}).copy()
    payment_info = request.session.get('payment_info', {}).copy()
    property = get_object_or_404(Properties, pk=property_id)

    if 'payment_option' in payment_info:
        payment_info['pay_method'] = payment_info.pop('payment_option')

    if request.method == 'POST':
        # Fetch the related offer first
        offer = PurchaseOffer.objects.filter(
            buyer=request.user,
            property=property,
            status__iexact='accepted'
        ).first()

        if not offer:
            return HttpResponse("No matching accepted offer found", status=400)

        # Create and save finalized offer all at once
        finalized = FinalizedOffer.objects.create(
            user=request.user,
            property=property,
            purchase_offer=offer,
            **contact_info,
            **payment_info
        )

        # Transfer ownership
        property.owner = request.user
        property.property_sold_status = True
        property.save()

        # Clean up
        request.session.pop('contact_info', None)
        request.session.pop('payment_info', None)

        return redirect('confirmation')

    return render(request, 'review.html', {
        'contact_info': contact_info,
        'payment_info': payment_info,
        'property': property
    })


    
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

    return redirect('property_detail', property_id=property_id)