from xml.etree.ElementInclude import include
from django.contrib import admin
from .models import *
from django.contrib.contenttypes.admin import GenericTabularInline
from django.db.models.functions import Lower
from django.contrib.sessions.models import Session
from . import forms
# Register your models here.



class CustomerAdmin(admin.ModelAdmin):
    model = Customer
    readonly_fields=['First_name',"Last_name",'Email','Phone_number']
    exclude=["Device"]

class MultiplierAdmin(admin.ModelAdmin):
    model = Multiplier
    
class OrderItemAdmin(admin.ModelAdmin):
    list_display=( 'Item','Color','Size','Done')
    exclude= ["Done","Customer"]







class OrderItemlInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ["Item","Color","Size","Quantity","Customer","Done"]
    extra = 0

class AddresslInline(admin.StackedInline):
    model = Address


class OrderAdmin(admin.ModelAdmin):
    model = Order
    list_display=('Customer', 'get_customer_email', 'Ref_code','Ordered_date')
    inlines = [OrderItemlInline]
    search_fields = ['Customer__Email','Customer__First_name','Ref_code']
    list_filter = [
            'Ordered',
            'Ordered_date',
            
        ]
    readonly_fields=['Shipping_address','Customer','Ordered_date','Delivered_date','Shipped_date',"Ordered"]



    @admin.display(ordering="Customer__Email",description="Email")
    def get_customer_email(self,obj):
        return obj.Customer.Email




    



class PictureInline(admin.StackedInline):
    model = Picture


class ProductAdmin(admin.ModelAdmin):
    model = Product
    
    list_display=('Name','SKU','Price')
    inlines = [PictureInline]
    search_fields = ['Name','SKU']
    list_filter = [
         "Category", 
    ]
    actions = ['multiplier','set_as_pick',"remove_as_pick"]

    exclude = ["PriceLBP"]

    def get_ordering(self, request):
        return [Lower('SKU')]
    
    def multiplier(self, request, queryset):
        from math import ceil
        multiplier = Multiplier.objects.all()[0]

        for product in queryset:
            product.Price.amount = ceil(float(product.PriceLBP.amount) / multiplier.USDtoLBP)  
            product.save(update_fields=['Price'])
    multiplier.short_description = "set new exchange rate"

    def set_as_pick(self,request,queryset):
        for product in queryset:
            product.Pick=True
            product.save(update_fields={"Pick"})
    set_as_pick.short_description = "choose as pick"

    def remove_as_pick(self,request,queryset):
        for product in queryset:
            product.Pick=False
            product.save(update_fields={"Pick"})
    remove_as_pick.short_description = "remove as pick"




class DiscoverAdmin(admin.ModelAdmin):
    # form = forms.DiscoverForm
    model = Discover
    list_display=('Title', )
    exclude = ['id']

    #inlines = [ProductlInline,]


class ProductAdminInLine(admin.TabularInline):
    model = Product
    extra = 0
    readonly_fields = ["Name", "SKU","Description","Size","Color","Price","Category","Status","Optional","Discover","Image","PriceLBP"]

class CollectionAdmin(admin.ModelAdmin):
    # form=forms.CollectionForm
    model = Collection
    list_display=('Title', )
    inlines = (ProductAdminInLine,)

class SessionAdmin(admin.ModelAdmin):
    def _session_data(self, obj):
        return obj.get_decoded()
    list_display = ['session_key', '_session_data', 'expire_date']


class CategoryAdmin(admin.ModelAdmin):
    model = Category
    list_display=('Name', )
    search_fields = ['Name']




class ContactUsAdmin(admin.ModelAdmin):
    
    list_display = ['Name', 'Email']
    readonly_fields = ["Name", "Email","Content"]


class NewsletterAdmin(admin.ModelAdmin):
    list_display = ['Email']
    readonly_fields = ["Email"]

    actions = ['get_email_list']

    def get_email_list(self,request,queryset):
        from django.http import HttpResponse
        f = open("email_list.txt", "w")
        email_list = []
        for email in queryset:
            email_list.append(email.Email)
        mailingList = ";".join(email_list)
        f.write(mailingList)
        f.close()
        f = open("email_list.txt", "r")
        response = HttpResponse(f, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename="email_list.txt"'
        return response
    get_email_list.short_description = "get email list"


class ZoneAdmin(admin.ModelAdmin):

    list_display = ['ZoneNumber', 'Cost']


class CountryAdmin(admin.ModelAdmin):

    list_display = ['Country', 'Zone']
    # readonly_fields = ["Country"]




admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Customer,CustomerAdmin)
admin.site.register(Order,OrderAdmin)
admin.site.register(OrderItem,OrderItemAdmin)
admin.site.register(Discover,DiscoverAdmin)
admin.site.register(Multiplier,MultiplierAdmin)
admin.site.register(ContactUs,ContactUsAdmin)
admin.site.register(Session, SessionAdmin)
admin.site.register(Collection, CollectionAdmin)
admin.site.register(Zone, ZoneAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(Newsletter, NewsletterAdmin)
#admin.site.register(ShippingAddress)
