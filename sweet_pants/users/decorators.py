from django.http import HttpResponse
from django.contrib.auth.models import Group
from django.shortcuts import redirect
from django.contrib.auth.mixins import AccessMixin

def is_purpose(view_func):
    def wrapped_func(request, *args, **kwargs):
        if Group.objects.filter(user = request.user):
            return view_func(request, *args, **kwargs)
        return redirect('purpose')
    return wrapped_func

def purpose(view_func):
    def wrapped_func(request, *args, **kwargs):
        if Group.objects.filter(user = request.user):
            return redirect('customer-homepage')
        return view_func(request, *args, **kwargs)
    return wrapped_func

def unauthenticated_user(view_func):
    def wrapped_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('customer-homepage')
        return view_func(request, *args, **kwargs)
    return wrapped_func

def allowed_users(allowed_roles=''):
    def decorator(view_func):
        def wrapped_func(request, *args, **kwargs):
            if allowed_roles == 'notvendor' and (not request.user.groups.all() or request.user.groups.all()[0].name == 'Customer'):
                return view_func(request, *args, **kwargs)
            elif request.user.groups.all()[0].name == allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return redirect('customer-homepage')
        return wrapped_func
    return decorator

class VendorRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        elif request.user.is_authenticated and not request.user.groups.all()[0].name == 'Vendor':
            return redirect ('customer-homepage')
        return super().dispatch(request, *args, **kwargs)