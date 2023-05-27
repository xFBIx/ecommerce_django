from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

class Profile_customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='customer_profile_pics')
    address = models.TextField(null = True)
    balance = models.FloatField(validators = [MinValueValidator(0.0)], default = 5000)

    def __str__(self):
        return f'{self.user.username} Customer Profile'

class Profile_vendor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='vendor_profile_pics')
    coupon = models.CharField(max_length=100, null = True, blank = True)
    discount_on_coupon_code = models.FloatField(validators = [MinValueValidator(0.0)], default = 0)

    def __str__(self):
        return f'{self.user.username} Vendor Profile'
