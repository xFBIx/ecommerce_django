from django.shortcuts import render, redirect
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from .models import Product, Items, Review
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from users.decorators import VendorRequiredMixin, is_purpose, PurposeRequiredMixin
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from users.decorators import allowed_users
from datetime import datetime
from .admin import VendorResource
from django.http import HttpResponse
from mailjet_rest import Client
from sweet_pants import keyconfig
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


@is_purpose
def contact(request):
    return render(request, "mainpage/contact.html")


@is_purpose
def about(request):
    return render(request, "mainpage/about.html")


@is_purpose
def FAQ(request):
    return render(request, "mainpage/faq.html")


from django.db.models import Q

class ProductListView(PurposeRequiredMixin, ListView):
    model = Product
    template_name = "mainpage/index_c.html"

    def get_queryset(self):
        queryset = Product.objects.all()
        
        search = self.request.GET.get('search')
        categories = self.request.GET.getlist('category')
        locations = self.request.GET.getlist('location')
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')

        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(category__icontains=search) |
                Q(location__icontains=search)
            )

        if categories:
            queryset = queryset.filter(category__in=categories)
        
        if locations:
            queryset = queryset.filter(location__in=locations)
        
        if min_price:
            queryset = queryset.filter(price__gte=float(min_price))
        
        if max_price:
            queryset = queryset.filter(price__lte=float(max_price))

        return queryset.order_by('-sales').distinct()

    def get_context_data(self, *args, **kwargs):
        context = super(ProductListView, self).get_context_data(*args, **kwargs)
        
        # Existing context logic
        if self.request.user.groups.all():
            if self.request.user.groups.all()[0].name == "Vendor":
                context["vendor"] = "vendor"
            else:
                context["customer"] = "customer"
        else:
            context["customer"] = "customer"

        user_list = self.get_queryset()
        page = self.request.GET.get("page", 1)

        paginator = Paginator(user_list, 6)
        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)
        context["customer_products"] = users

        if self.request.user.is_authenticated:
            userr_list = self.get_queryset().filter(vendor=self.request.user.id)
            pagee = self.request.GET.get("page", 1)

            paginatorr = Paginator(userr_list, 3)
            try:
                userss = paginatorr.page(pagee)
            except PageNotAnInteger:
                userss = paginatorr.page(1)
            except EmptyPage:
                userss = paginatorr.page(paginatorr.num_pages)
            context["vendor_products"] = userss

        # Add these lines
        CATEGORY_CHOICES = [
            ("Sofas", "Sofas"),
            ("Chairs", "Chairs"),
            ("Tables", "Tables"),
            ("Beds", "Beds"),
            ("Cupboards", "Cupboards"),
        ]
        LOCATION_CHOICES = [
            ("Ahmedabad", "Ahmedabad"),
            ("Bangalore", "Bangalore"),
            ("Delhi", "Delhi"),
            ("Mumbai", "Mumbai"),
            ("Pune", "Pune"),
        ]
        context['selected_categories'] = self.request.GET.getlist('category')
        context['selected_locations'] = self.request.GET.getlist('location')
        context['CATEGORY_CHOICES'] = CATEGORY_CHOICES
        context['LOCATION_CHOICES'] = LOCATION_CHOICES

        return context


class ProductDetailView(PurposeRequiredMixin, UserPassesTestMixin, DetailView):
    model = Product
    template_name = "mainpage/product_detail.html"

    def post(self, request, pk, **kwargs):
        product = Product.objects.filter(id=pk).first()
        quantity = int(request.POST.get("product-quantity"))
        if not request.user.shoppingcart.orderitems.filter(
            item=product, is_ordered=False
        ):
            if quantity > product.quantity:
                messages.warning(
                    request,
                    f"{quantity} quantities of this product is not available please select lesser",
                )
                return redirect("product-detail", pk=pk)
            item = Items.objects.create(
                item=product, quantity=quantity, customer=request.user
            )
            request.user.shoppingcart.orderitems.add(item)
            request.user.shoppingcart.save()
            messages.success(request, "Product successfully added to Shopping Cart")
            return redirect("product-detail", pk=pk)
        else:
            messages.info(request, "Product is already present in your shopping cart")
            return redirect("product-detail", pk=pk)

    def test_func(self):
        product = self.get_object()
        if self.request.user.groups.all():
            if self.request.user.groups.all()[0].name == "Vendor":
                if self.request.user == product.vendor:
                    return True
                return False
            else:
                return True
        else:
            return True


class ProductCreateView(VendorRequiredMixin, CreateView):
    model = Product
    template_name = "mainpage/product_create.html"
    fields = ["image", "title", "description", "price", "quantity", "discount", "category", "location"]

    def form_valid(self, form):
        form.instance.vendor = self.request.user
        form.instance.discounted_price = (
            form.instance.price - form.instance.price * form.instance.discount / 100
        )
        return super().form_valid(form)


class ProductUpdateView(VendorRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    template_name = "mainpage/product_edit.html"
    fields = fields = ["image", "title", "description", "price", "quantity", "discount", "category", "location"]

    def form_valid(self, form):
        form.instance.vendor = self.request.user
        form.instance.discounted_price = (
            form.instance.price - form.instance.price * form.instance.discount / 100
        )
        return super().form_valid(form)

    def test_func(self):
        product = self.get_object()
        if self.request.user == product.vendor:
            return True
        return False


class ProductDeleteView(VendorRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    template_name = "mainpage/product_delete.html"
    success_url = "/"

    def test_func(self):
        product = self.get_object()
        if self.request.user == product.vendor:
            return True
        return False


@is_purpose
@allowed_users(allowed_roles="notvendor")
def vendors(request):
    context = {"vendors": User.objects.all().filter(groups__name="Vendor")}
    return render(request, "mainpage/vendors.html", context)


@is_purpose
@allowed_users(allowed_roles="notvendor")
def vendor_products(request, pk):
    context = {
        "products": Product.objects.all().filter(vendor=pk).order_by("-sales"),
        "vendor": User.objects.all().filter(id=pk).first(),
    }
    return render(request, "mainpage/vendor_products.html", context)


@login_required
@is_purpose
@allowed_users(allowed_roles="Customer")
def add_to_wishlist(request, pk):
    item = Product.objects.filter(id=pk).first()
    if item in request.user.wishlist.items.all():
        messages.info(request, "Product is already present in the Wishlist")
        return redirect("customer-homepage")
    request.user.wishlist.items.add(item)
    messages.success(request, "Product successfully added to Wishlist")
    return redirect("customer-homepage")


@login_required
@is_purpose
@allowed_users(allowed_roles="Customer")
def remove_wishlist(request, pk):
    item_to_remove = Product.objects.filter(id=pk).first()
    if item_to_remove in request.user.wishlist.items.all():
        request.user.wishlist.items.remove(item_to_remove)
        messages.success(request, "Product has been removed from Wishlist successfully")
        return redirect("wishlist")
    else:
        return redirect("customer-homepage")


@login_required
@is_purpose
@allowed_users(allowed_roles="Customer")
def shoppingcart(request):
    context = {
        "items": request.user.shoppingcart.orderitems.all().filter(is_ordered=False),
        "total": request.user.shoppingcart.get_cart_total(),
    }
    return render(request, "mainpage/shoppingcart.html", context)


@login_required
@is_purpose
@allowed_users(allowed_roles="Customer")
def wishlist(request):
    context = {"items": request.user.wishlist.items.all()}
    return render(request, "mainpage/wishlist.html", context)


@login_required
@is_purpose
@allowed_users(allowed_roles="Customer")
def remove_shoppingcart(request, pk):
    product = Product.objects.filter(id=pk).first()
    item_to_delete = request.user.shoppingcart.orderitems.filter(
        item=product, is_ordered=False
    )
    if item_to_delete.exists():
        item_to_delete[0].delete()
        messages.success(request, "Product has been removed from Shopping Cart")
    return redirect("shoppingcart")


@login_required
@is_purpose
@allowed_users(allowed_roles="Customer")
def checkout(request):
    context = {
        "address": request.user.profile_customer.address,
        "no_address": "Please add an address before placing order!",
        "balance": request.user.profile_customer.balance,
        "items": request.user.shoppingcart.orderitems.all().filter(is_ordered=False),
        "total": request.user.shoppingcart.get_cart_coupon(),
    }
    return render(request, "mainpage/checkout.html", context)


@login_required
@is_purpose
@allowed_users(allowed_roles="Customer")
def coupon(request, pk):
    product = Product.objects.filter(id=pk).first()
    item = request.user.shoppingcart.orderitems.get(item=product, is_ordered=False)
    if item.is_coupon == True:
        messages.warning(request, "Coupon code already applied")
        return redirect("checkout")
    else:
        if request.method == "POST":
            code = request.POST.get("coupon")
            if product.vendor.profile_vendor.coupon == code:
                item.is_coupon = True
                item.save()
                messages.success(request, "Coupon code successfully applied!")
                return redirect("checkout")
            else:
                messages.warning(request, "No such coupon code exists for this vendor")
                return redirect("checkout")
        return render(request, "mainpage/coupon.html")


@login_required
@is_purpose
@allowed_users(allowed_roles="Customer")
def addtocart(request, pk):
    product = Product.objects.filter(id=pk).first()
    if request.method == "POST":
        quantity = int(request.POST.get("product-quantity"))
        if not request.user.shoppingcart.orderitems.filter(
            item=product, is_ordered=False
        ):
            if quantity > product.quantity:
                messages.warning(
                    request,
                    f"{quantity} quantities of this product is not available please select lesser",
                )
                return redirect("wishlist")
            item = Items.objects.create(
                item=product, quantity=quantity, customer=request.user
            )
            request.user.shoppingcart.orderitems.add(item)
            request.user.shoppingcart.save()
            messages.success(request, "Product successfully added to Shopping Cart")
            return redirect("wishlist")
        else:
            messages.info(request, "Product is already present in your shopping cart")
            return redirect("wishlist")
    return render(request, "mainpage/addtocart.html")


@login_required
@is_purpose
@allowed_users(allowed_roles="Customer")
def updatecart(request, pk):
    product = Product.objects.filter(id=pk).first()
    if request.method == "POST":
        quantity = int(request.POST.get("product-quantity"))
        if request.user.shoppingcart.orderitems.filter(item=product, is_ordered=False):
            if quantity > product.quantity:
                messages.warning(
                    request,
                    f"{quantity} quantities of this product is not available please select lesser",
                )
                return redirect("shoppingcart")
            data = request.user.shoppingcart.orderitems.filter(
                item=product, is_ordered=False
            ).first()
            data.quantity = quantity
            data.save()
            messages.success(request, "Product quantity has been successfully updated")
            return redirect("shoppingcart")
        else:
            return redirect("customer-homepage")
    return render(request, "mainpage/updatecart.html")


@login_required
@is_purpose
@allowed_users(allowed_roles="Customer")
def removecoupon(request, pk):
    product = Product.objects.filter(id=pk).first()
    item = request.user.shoppingcart.orderitems.get(item=product, is_ordered=False)
    if item.is_coupon == False:
        messages.warning(request, "No coupon is applied!")
        return redirect("checkout")
    else:
        item.is_coupon = False
        item.save()
        messages.success(request, "Coupon code successfully removed!")
        return redirect("checkout")


def mail(vendor_email, vendor, customer, quantity, product, amount):
    API_KEY = keyconfig.MJ_APIKEY_PUBLIC
    API_SECRET = keyconfig.MJ_APIKEY_PRIVATE
    mailjet = Client(auth=(API_KEY, API_SECRET), version="v3.1")
    data = {
        "Messages": [
            {
                "From": {"Email": "rudradattdave@gmail.com", "Name": "Sweet Pants"},
                "To": [{"Email": f"{vendor_email}", "Name": f"{vendor}"}],
                "Subject": "New order has been placed for your product",
                "TextPart": f"Greetings from Sweet Pants. {customer} has placed order for {quantity} pieces of {product} with total price of Rs.{amount}",
            }
        ]
    }
    mailjet.send.create(data=data)


@login_required
@is_purpose
@allowed_users(allowed_roles="Customer")
def buynow(request):
    if request.user.shoppingcart.orderitems.all().filter(is_ordered=False):
        if not request.user.profile_customer.address:
            messages.warning(request, "Please add an delivery address first")
            return redirect("checkout")
        for item in request.user.shoppingcart.orderitems.filter(is_ordered=False):
            if item.quantity > item.item.quantity:
                messages.warning(
                    request,
                    f"{item.quantity} quantities of this product is not available please select lesser",
                )
                return redirect("checkout")
        if (
            request.user.profile_customer.balance
            < request.user.shoppingcart.get_cart_coupon()
        ):
            messages.warning(
                request, "Insufficient account balance, Please add balance"
            )
            return redirect("checkout")
        request.user.profile_customer.balance -= (
            request.user.shoppingcart.get_cart_coupon()
        )
        request.user.profile_customer.save()
        for item in request.user.shoppingcart.orderitems.filter(is_ordered=False):
            item.item.sales += item.quantity
            item.item.quantity -= item.quantity
            item.item.save()
            item.orderdate = datetime.now()
            if item.is_coupon:
                item.orderprice = (
                    item.item.discounted_price
                    - item.item.discounted_price
                    * item.item.vendor.profile_vendor.discount_on_coupon_code
                    / 100
                ) * item.quantity
            else:
                item.orderprice = item.item.discounted_price * item.quantity
            item.is_ordered = True
            item.save()
            mail(
                item.item.vendor.email,
                item.item.vendor.username,
                request.user.username,
                item.quantity,
                item.item.title,
                item.orderprice,
            )

        return render(request, "mainpage/confirmation.html")
    else:
        return redirect("customer-homepage")


@login_required
@is_purpose
@allowed_users(allowed_roles="Customer")
def orderscustomer(request):
    context = {
        "orders": request.user.shoppingcart.orderitems.filter(is_ordered=True).order_by(
            "-orderdate"
        )
    }
    return render(request, "mainpage/orders-customer.html", context)


@login_required
@is_purpose
@allowed_users(allowed_roles="Vendor")
def ordersvendor(request):
    items = Items.objects.filter(is_ordered=True).order_by("-orderdate")
    order = []
    for item in items:
        if item.item.vendor == request.user:
            order.append(item)
    context = {"orders": order}
    return render(request, "mainpage/orders-vendor.html", context)


@login_required
@is_purpose
@allowed_users(allowed_roles="Customer")
def review(request, pk):
    product = Product.objects.filter(id=pk).first()
    print(request.user.shoppingcart.orderitems.filter(is_ordered=True))
    print(product)
    if request.user.shoppingcart.orderitems.filter(item=product, is_ordered=True):
        if request.method == "POST":
            review = request.POST.get("review")
            Review.objects.create(
                product=product,
                description=review,
                date=datetime.now(),
                customer=request.user,
            )
            messages.success(request, "Your review has been posted!")
            return redirect("orders-customer")
        return render(request, "mainpage/review.html")
    else:
        return redirect("orders-customer")


@login_required
@is_purpose
@allowed_users(allowed_roles="Vendor")
def download_orders(request):
    rawdata = VendorResource()
    queryset = Items.objects.filter(is_ordered=True).filter(item__vendor=request.user)
    dataset = rawdata.export(queryset)
    response = HttpResponse(dataset.xls, content_type="application/vnd.ms-excel")
    response["Content-Discription"] = "attachment; filename='orders.xls'"
    return response
