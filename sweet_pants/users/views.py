from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ProfileCustomerUpdateForm, ProfileVendorUpdateForm, purposeform
from django.contrib.auth.decorators import login_required
from .models import Profile_customer, Profile_vendor
from mainpage.models import ShoppingCart, Wishlist
from .decorators import unauthenticated_user, allowed_users, purpose, is_purpose
import string
import random

@login_required
@purpose
def purpose(request):
    if request.method == 'POST':
        form = purposeform(request.POST)
        if form.is_valid():
            user_group = form.cleaned_data.get('purpose')
            request.user.groups.add(user_group)
            
            if request.user.groups.all()[0].name == 'Customer' :
                Profile_customer.objects.create(user = request.user)
                request.user.profile_customer.save()
                
                ShoppingCart.objects.create(user = request.user)
                request.user.shoppingcart.save()
                
                Wishlist.objects.create(user = request.user)
                request.user.wishlist.save()
                
            elif request.user.groups.all()[0].name == 'Vendor' :
                Profile_vendor.objects.create(user = request.user)
                request.user.profile_vendor.save()
            
            return redirect('customer-homepage')
    context ={}
    context['form']= purposeform()
    return render(request, "users/purpose.html", context)

#no longer needed after google allauth
'''
@unauthenticated_user
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user_group = form.cleaned_data.get('purpose')
            user.groups.add(user_group)
            username = form.cleaned_data.get('username')
            
            if user.groups.all()[0].name == 'Customer' :
                Profile_customer.objects.create(user = user)
                user.profile_customer.save()
                
                ShoppingCart.objects.create(user = user)
                user.shoppingcart.save()
                
                Wishlist.objects.create(user = user)
                user.wishlist.save()
                
            elif user.groups.all()[0].name == 'Vendor' :
                Profile_vendor.objects.create(user = user)
                user.profile_vendor.save()
            
            messages.success(request, f'Account has been created for {username}! You can now log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})
'''

@login_required
@is_purpose
def profile(request):
    if request.user.groups.all()[0].name == 'Customer' :
        context = {'address' : request.user.profile_customer.address,
                   'balance' : request.user.profile_customer.balance , 'no_address' : 'No Address !' }
        if request.user.profile_customer.image:
            context['image'] =  request.user.profile_customer.image.url
    elif request.user.groups.all()[0].name == 'Vendor' :
        context = {'coupon' : request.user.profile_vendor.coupon,
                   'no_coupon' : 'No Coupon Code!', 'dis_coup' : request.user.profile_vendor.discount_on_coupon_code }
        if request.user.profile_vendor.image:
            context['image'] =  request.user.profile_vendor.image.url
    return render(request, 'users/profile.html', context)

@login_required
@is_purpose
def edit_profile(request):
    if request.method == 'POST':
        if request.user.groups.all()[0].name == 'Customer' :
            form = ProfileCustomerUpdateForm(request.POST, request.FILES, instance=request.user.profile_customer)
        elif request.user.groups.all()[0].name == 'Vendor' :
            form = ProfileVendorUpdateForm(request.POST, request.FILES, instance=request.user.profile_vendor)
        if form.is_valid() :
            form.save()
            messages.success(request, f'Your profile details has been updated!')
            return redirect('profile')
    else :
        if request.user.groups.all()[0].name == 'Customer' :
            form = ProfileCustomerUpdateForm(instance=request.user.profile_customer)
        elif request.user.groups.all()[0].name == 'Vendor' :
            form = ProfileVendorUpdateForm(instance=request.user.profile_vendor)
    
    
    return render(request, 'users/edit-profile.html', {'form' : form })

@login_required
@allowed_users(allowed_roles='Vendor')
def generate_coupon(request):
    res = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    request.user.profile_vendor.coupon = res
    request.user.profile_vendor.save()
    messages.success(request, f'Coupon Code has been successfully generated!')
    return redirect('profile')

@login_required
@allowed_users(allowed_roles='Vendor')
def remove_coupon(request):
    res = ''
    request.user.profile_vendor.coupon = res
    request.user.profile_vendor.save()
    messages.success(request, f'Coupon Code has been successfully removed!')
    return redirect('profile')