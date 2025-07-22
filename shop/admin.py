from django.contrib import admin
from .models import CustomUser, Category, Card, Product, SealedProduct, Listing
from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelAdmin
# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Listing)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'order', 'slug')
    list_editable = ('order',)
    list_filter = ('parent',)
    search_fields = ('name',)

    fieldsets = (
        (None, {'fields': ('name', 'parent', 'order')}),
        ('Advanced', {'fields': ('slug',)}),
    )
    readonly_fields = ('slug',)

@admin.register(Product)
class ProductAdmin(PolymorphicParentModelAdmin):
    base_model = Product
    child_models = (Card,SealedProduct,)




class CardAdmin(PolymorphicChildModelAdmin):
    base_model = Card

admin.site.register(Card, CardAdmin)


class SealedProductAdmin(PolymorphicChildModelAdmin):
    base_model = SealedProduct
admin.site.register(SealedProduct, SealedProductAdmin)