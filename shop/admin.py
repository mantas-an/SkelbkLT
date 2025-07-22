from django.contrib import admin
from .models import CustomUser, Category, Card, Product, SealedProduct
from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelAdmin
# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Category)

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