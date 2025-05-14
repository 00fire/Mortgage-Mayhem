# app2/decorators.py

from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required

def seller_required(view_func):
    @login_required
    def _wrapped(request, *args, **kwargs):
        if request.user.profile.role != 'seller':
            raise PermissionDenied("Only sellers can do that.")
        return view_func(request, *args, **kwargs)
    return _wrapped

def buyer_required(view_func):
    @login_required
    def _wrapped(request, *args, **kwargs):
        if request.user.profile.role != 'buyer':
            raise PermissionDenied("Only buyers can do that.")
        return view_func(request, *args, **kwargs)
    return _wrapped
