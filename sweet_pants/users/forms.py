from django import forms
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm
from mainpage.models import ShoppingCart, Wishlist
from .models import Profile_customer, Profile_vendor
from allauth.account.forms import SignupForm

class purposeform(forms.Form):
    purpose = forms.ModelChoiceField(queryset=Group.objects.all(), required=True,help_text="DO YOU WANT TO SIGN UP AS A CUSTOMER OR A VENDOR?")
 
class CustomSignupForm(SignupForm):
    purpose = forms.ModelChoiceField(queryset=Group.objects.all(), required=True, help_text="DO YOU WANT TO SIGN UP AS A CUSTOMER OR A VENDOR?")
 
    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        user_group = self.cleaned_data.get('purpose')
        user.groups.add(user_group)
        user.save()
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
        return user

#no longer needed after google allauth
'''
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    purpose = forms.ModelChoiceField(queryset=Group.objects.all(), required=True,help_text="DO YOU WANT TO SIGN UP AS A CUSTOMER OR A VENDOR?")
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'purpose']
'''
        
class ProfileCustomerUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile_customer
        fields = ['image', 'address', 'balance']
        
        
class ProfileVendorUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile_vendor
        fields = ['image', 'discount_on_coupon_code']
