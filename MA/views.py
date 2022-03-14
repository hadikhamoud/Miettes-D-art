from django.shortcuts import render
from django.db import models
import random
import string
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from . import forms, models
from django.http import HttpResponseRedirect
from django.contrib.auth.models import Group
from django.contrib import auth
from django.contrib.auth.decorators import login_required, user_passes_test
from datetime import datetime, timedelta, date
from django.core.mail import send_mail
from miettes.settings import EMAIL_HOST_USER
from django.conf import settings
from django.contrib.gis.geoip2 import GeoIP2


def get_total_and_items(queryset):
    total = 0
    number = 0
    for item in queryset:
        number += item.Quantity
        total += item.Item.PriceLBP * item.Quantity
    return total, number


def get_country(request):
    g = GeoIP2()
    US = True
    ip = request.META.get('REMOTE_ADDR', None)
    if ip:
        Country = g.city(ip)['country_code']
        if Country == 'LB':
            US = False
    else:
        Country = 'US'
        
    return Country, US






def generate_Ref_code():
    current_date = datetime.now()
    Ref_code = str(int(current_date.strftime("%y%m%d")))+''.join(
        random.choice(string.ascii_uppercase + string.digits) for _ in range(4))
    return Ref_code


# Create your views here.
def homepage(request):
    Discovers = models.Discover.objects.all()
    return render(request, 'miettes/index.html', {'Discovers': Discovers})


def aboutus_view(request):
    return render(request, 'miettes/aboutus.html')


def contactus_view(request):
    if request.method == 'POST':
        email = request.POST.get("email")
        name = request.POST.get("name")
        subject = request.POST.get("subject")
        send_mail(str(name)+' || '+str(email), subject,
                  EMAIL_HOST_USER, ['support@miettesdart.com'])

        return render(request, 'miettes/contactus.html')

    return render(request, 'miettes/contactus.html')


def products_view(request):
    #Country, US = get_country(request)
    Allproducts = models.Product.objects.all()
    return render(request, 'miettes/productsgrid.html', {'Allproducts': Allproducts})
# def searchbooksadmin(request):
#     #get the search input as POST
    
#         #search by book name

#         Books = models.Book.objects.filter(name__contains = searched).filter(Active =True)
#         try:
#             #search by isbn, ignore query if input is not int
#             Booksbyisbn = models.Book.objects.filter(isbn__contains = int(searched)).filter(Active =True)
#             print(Booksbyisbn)
#         except:
#             Booksbyisbn = models.Book.objects.none()
#         #merge both queries
#         Books = list(chain(Books,Booksbyisbn))
#         print("books",Books)
#         return render(request, 'library/searchbooksadmin.html',{'books':Books})



def productsearch_view(request):
    #Country, US = get_country(request)
    if request.method == "POST":
        searched = request.POST['searched']
        ProductsQuery = models.Product.objects.filter(Name__contains = searched)
        return render(request, 'miettes/productsearch.html', {'Allproducts': ProductsQuery,'Query':searched})
    return render(request, 'miettes/productsearch.html')


def discover_view(request, Title):
    discover = models.Discover.objects.get(Title=Title)
    Allproducts = discover.Items.all()
    print(Allproducts)
    return render(request, 'miettes/discover.html', {'Allproducts': Allproducts})


def viewproduct_view(request, SKU):
    Selectedproduct = models.Product.objects.filter(SKU=SKU)[0]
    Pictures = models.Picture.objects.filter(Product=Selectedproduct)
    if not Pictures.exists():
        Pictures = models.Picture.objects.none()

    if request.method == "POST":
        Color_choice = request.POST.getlist("color")
        Size_choice = request.POST.getlist("size")

        try:
            customer = request.user.customer
        except:
            Device = request.COOKIES['device']
            customer, created = models.Customer.objects.get_or_create(
                Device=Device)

        order, created = models.Order.objects.get_or_create(
            Customer=customer, Ordered=False)
        orderitem, created = models.OrderItem.objects.get_or_create(
            Customer=customer, Order=order, Item=Selectedproduct, Color=Color_choice, Size=Size_choice)
        orderitem.save()
        order.save()

    return render(request, 'miettes/viewproduct.html', {'Selectedproduct': Selectedproduct, 'Pictures': Pictures})


def cart_view(request):
    try:
        customer = request.user.customer
    except:
        Device = request.COOKIES['device']
        customer, created = models.Customer.objects.get_or_create(
            Device=Device)
        print(created)
    order, created = models.Order.objects.get_or_create(
        Customer=customer, Ordered=False)
    orderitems = models.OrderItem.objects.filter(Order=order.pk)
    total, numberofitems = get_total_and_items(orderitems)
    if request.method == 'POST':
        Name = request.POST.get('number')
        print(Name)
        

    return render(request, 'miettes/cart.html', {'Order': orderitems, "total": total, "numberofitems": numberofitems})
    


def removeitem_view(request, orderItemID):
    orderItem = models.OrderItem.objects.get(id=int(orderItemID))
    orderItem.delete()
    return redirect('cart')


def checkout_view(request):
    try:
        customer = request.user.customer
    except:
        Device = request.COOKIES['device']
        customer, created = models.Customer.objects.get_or_create(
                Device=Device)
    form = forms.AddressForm()
    order, created = models.Order.objects.get_or_create(
        Customer=customer, Ordered=False)
    orderitems = models.OrderItem.objects.filter(Order=order.pk)
    total, numberofitems = get_total_and_items(orderitems)
    if request.method == "POST":
        form = forms.AddressForm(request.POST)
        Name = request.POST.get("firstname")
        Email = request.POST.get("email")
        customer.Name = Name
        customer.Email = Email
        customer.save()
        print('you are in post')
        print(form)

        if form.is_valid():
            Address = form.save()
            print("you are in form")
            
            order.Shipping_address = models.Address.objects.create(Country=Address.Country,Street_address=Address.Street_address,Zip=Address.Zip)
            #address, created = models.Address.get_or_create(Customer = customer, Street_address = )
            order.Ordered = True
            order.Ordered_date = datetime.now()
            order.Total = total
            order.Customer = customer
            order.save()
            return render(request, 'miettes/thankyou.html')
    return render(request, 'miettes/checkout.html', {'Order': orderitems, 'form': form,"total": total, "numberofitems": numberofitems})


def thankyou_view(request):
    return render(request, 'miettes/thankyou.html')


def addproduct_view(request):
    form = forms.ProductForm()
    if request.method == 'POST':
        form = forms.ProductForm(request.POST, request.FILES)
        if form.is_valid():
            Product = form.save()
