from import_export.admin import ImportExportModelAdmin
from django.contrib.auth.models import User
from django.contrib import admin
from .models import Product, ShoppingCart, Wishlist, Items, Review
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget

admin.site.register(Product)
admin.site.register(ShoppingCart)
admin.site.register(Wishlist)
admin.site.register(Review)

class VendorResource(resources.ModelResource):
    
    Customer = fields.Field(
        column_name='Customer',
        attribute='customer',
        widget=ForeignKeyWidget(User, field='username'))
    Product = fields.Field(
        column_name='Product',
        attribute='item',
        widget=ForeignKeyWidget(Product, field='title'))

    class Meta:
        model = Items
        exclude = ('id','customer','item','is_ordered', )

class ItemsResource(resources.ModelResource):
    
    Customer = fields.Field(
        column_name='Customer',
        attribute='customer',
        widget=ForeignKeyWidget(User, field='username'))
    Product = fields.Field(
        column_name='Product',
        attribute='item',
        widget=ForeignKeyWidget(Product, field='title'))
    Vendor = fields.Field(
        column_name='Vendor',
        attribute='item',
        widget=ForeignKeyWidget(Product, field='vendor'))

    class Meta:
        model = Items
        exclude = ('id','customer','item','is_ordered', )

class ItemsAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_classes = [ItemsResource]
    def get_export_queryset(self, request):
            return Items.objects.filter(is_ordered=True)
    
admin.site.register(Items, ItemsAdmin)