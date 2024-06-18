from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
from PIL import Image


class Product(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(null=True, blank=True, upload_to="product_pics")
    vendor = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.FloatField(
        validators=[MinValueValidator(0.0)], null=False, blank=False
    )
    quantity = models.PositiveIntegerField(null=False, blank=False)
    discount = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(99)], default=0
    )
    sales = models.PositiveIntegerField(default=0)
    discounted_price = models.FloatField(default=0)

    def save(self, *args, **kwargs):
        super(Product, self).save(*args, **kwargs)
        if self.image:
            img = Image.open(self.image.path)
            if img.height > 600 or img.width > 500:
                output_size = (600, 500)
                img.thumbnail(output_size)
                img.save(self.image.path)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("product-detail", kwargs={"pk": self.pk})


class Items(models.Model):
    customer = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)], default=1)
    is_ordered = models.BooleanField(default=False)
    orderdate = models.DateTimeField(null=True, blank=True)
    is_coupon = models.BooleanField(default=False)
    orderprice = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.item.title


class ShoppingCart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    orderitems = models.ManyToManyField(Items, blank=True)

    def get_cart_total(self):
        return sum(
            [
                item.item.discounted_price * item.quantity
                for item in self.orderitems.filter(is_ordered=False)
            ]
        )

    def get_cart_coupon(self):
        sum = 0
        for item in self.orderitems.filter(is_ordered=False):
            if item.is_coupon:
                sum += (
                    item.item.discounted_price
                    - item.item.discounted_price
                    * item.item.vendor.profile_vendor.discount_on_coupon_code
                    / 100
                ) * item.quantity
            else:
                sum += item.item.discounted_price * item.quantity
        return sum

    def __str__(self):
        return self.user.username


class Wishlist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(Product, blank=True)

    def __str__(self):
        return self.user.username


class Review(models.Model):
    customer = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, related_name="reviews", on_delete=models.CASCADE
    )
    description = models.TextField()
    date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.product.title
