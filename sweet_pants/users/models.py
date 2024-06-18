from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from PIL import Image


class Profile_customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True, upload_to="customer_profile_pics")
    address = models.TextField(null=True)
    balance = models.FloatField(validators=[MinValueValidator(0.0)], default=5000)

    def save(self, *args, **kwargs):
        super(Profile_customer, self).save(*args, **kwargs)
        if self.image:
            img = Image.open(self.image.path)
            if img.height > 250 or img.width > 250:
                output_size = (250, 250)
                img.thumbnail(output_size)
                img.save(self.image.path)

    def __str__(self):
        return f"{self.user.username} Customer Profile"


class Profile_vendor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True, upload_to="vendor_profile_pics")
    coupon = models.CharField(max_length=100, null=True, blank=True)
    discount_on_coupon_code = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(99)], default=0
    )

    def save(self, *args, **kwargs):
        super(Profile_vendor, self).save(*args, **kwargs)
        if self.image:
            img = Image.open(self.image.path)
            if img.height > 250 or img.width > 250:
                output_size = (250, 250)
                img.thumbnail(output_size)
                img.save(self.image.path)

    def __str__(self):
        return f"{self.user.username} Vendor Profile"
