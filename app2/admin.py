from django.contrib import admin
from .models import UserProfile
from .models import Properties
from .models import PropertyImage
from .models import PurchaseOffer
from .models import FinalizedOffer
# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Properties)
admin.site.register(PropertyImage)
admin.site.register(PurchaseOffer)
admin.site.register(FinalizedOffer)