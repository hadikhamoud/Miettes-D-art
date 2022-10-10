from django.contrib import admin
from .models import *
from django.contrib.contenttypes.admin import GenericTabularInline
from django.db.models.functions import Lower
from django.contrib.sessions.models import Session

# Register your models here.



class CustomerAdmin(admin.ModelAdmin):
    model = Customer
    readonly_fields=['Name','Email','Device']

class MultiplierAdmin(admin.ModelAdmin):
    model = Multiplier
    
class OrderItemAdmin(admin.ModelAdmin):
    list_display=( 'Item','Color','Size','Done')







class OrderItemlInline(admin.TabularInline):
    model = OrderItem

class AddresslInline(admin.StackedInline):
    model = Address


class OrderAdmin(admin.ModelAdmin):
    model = Order
    list_display=('Customer', 'Ref_code','Total','Ordered_date')
    inlines = [OrderItemlInline]
    search_fields = ['Customer__Name','Ref_code']
    list_filter = [
            'Ordered',
        ]
    readonly_fields=['Shipping_address','Customer','Ordered_date']
    



class PictureInline(admin.StackedInline):
    model = Picture


class ProductAdmin(admin.ModelAdmin):
    model = Product
    list_display=('Name','SKU','PriceLBP','Price')
    inlines = [PictureInline]
    search_fields = ['Name','SKU']
    list_filter = [
         "Category", 
    ]
    actions = ['multiplier']

    def get_ordering(self, request):
        return [Lower('SKU')]
    
    def multiplier(self, request, queryset):
        from math import ceil
        multiplier = Multiplier.objects.all()[0]

        for product in queryset:
            product.Price.amount = ceil(float(product.PriceLBP.amount) / multiplier.USDtoLBP)  
            product.save(update_fields=['Price'])
    multiplier.short_description = "set new exchange rate"




class DiscoverAdmin(admin.ModelAdmin):
    model = Discover
    list_display=('Title', )
    #inlines = [ProductlInline,]



class SessionAdmin(admin.ModelAdmin):
    def _session_data(self, obj):
        return obj.get_decoded()
    list_display = ['session_key', '_session_data', 'expire_date']




admin.site.register(Product, ProductAdmin)
admin.site.register(Customer,CustomerAdmin)
admin.site.register(Order,OrderAdmin)
admin.site.register(OrderItem,OrderItemAdmin)
admin.site.register(Discover,DiscoverAdmin)
admin.site.register(Multiplier,MultiplierAdmin)
admin.site.register(Session, SessionAdmin)

#admin.site.register(ShippingAddress)
