from import_export.admin import ImportExportModelAdmin
from django.contrib.auth.models import User
from django.contrib import admin
from .models import Product, ShoppingCart, Wishlist, Items, Review, Book, BorrowRecord
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget

admin.site.register(Product)
admin.site.register(ShoppingCart)
admin.site.register(Wishlist)
admin.site.register(Review)
admin.site.register(Book)
admin.site.register(BorrowRecord)


class LibrarianResource(resources.ModelResource):

    User = fields.Field(
        column_name="User",
        attribute="customer",
        widget=ForeignKeyWidget(User, field="username"),
    )
    Product = fields.Field(
        column_name="Product",
        attribute="item",
        widget=ForeignKeyWidget(Product, field="title"),
    )

    class Meta:
        model = Items
        exclude = (
            "id",
            "customer",
            "item",
            "is_ordered",
        )


class ItemsResource(resources.ModelResource):

    User = fields.Field(
        column_name="User",
        attribute="customer",
        widget=ForeignKeyWidget(User, field="username"),
    )
    Product = fields.Field(
        column_name="Product",
        attribute="item",
        widget=ForeignKeyWidget(Product, field="title"),
    )
    Librarian = fields.Field(
        column_name="Librarian",
        attribute="item",
        widget=ForeignKeyWidget(Product, field="vendor"),
    )

    class Meta:
        model = Items
        exclude = (
            "id",
            "customer",
            "item",
            "is_ordered",
        )


class ItemsAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_classes = [ItemsResource]

    def get_export_queryset(self, request):
        return Items.objects.filter(is_ordered=True)


admin.site.register(Items, ItemsAdmin)
