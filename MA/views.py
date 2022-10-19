from django.shortcuts import render
from django.db import models
from django.shortcuts import redirect
from . import forms, models

# from django.http import HttpResponseRedirect
# from django.contrib.auth.models import Group
# from django.contrib import auth
# from django.contrib.auth.decorators import login_required, user_passes_test
# from django.conf import settings
# from django.contrib.gis.geoip2 import GeoIP2
# from django.utils.html import strip_tags


from django.core.mail import send_mail
from miettes.settings import EMAIL_HOST_USER
from .utils import *
from django.template.loader import render_to_string
import os

# Create your views here.


def homepage(request):
    Discovers = models.Discover.objects.all()
    return render(request, 'miettes/index.html', {'Discovers': Discovers})


def base_dev(request):
    return render(request, 'miettes/basedev.html')


def aboutus_view(request):
    return render(request, 'miettes/aboutus.html')


def contactus_view(request):
    if request.method == 'POST':
        email = request.POST.get("email")
        name = request.POST.get("name")
        content = request.POST.get("content")
        contact = models.ContactUs.objects.get_or_create(Name = name, Email = email, Content = content)
        send_html_mail(subject= "we have received your complaint", html_content="<h1> we love you<h1>",recipient_list=[email],sender=os.environ.get("EMAIL_HOST_USER_NOREPLY"))
        return render(request, 'miettes/contactus.html',{"sent": True})

    return render(request, 'miettes/contactus.html')


def products_view(request):
    #Country, US = get_country(request)
    Allproducts = models.Product.objects.all()
    return render(request, 'miettes/productsgrid.html', {'Allproducts': Allproducts})


   #_______________________________________For Searching____________________________ 
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

#_______________________________________For Searching____________________________




def productsearch_view(request):
    #Country, US = get_country(request)
    if request.method == "POST":
        searched = request.POST['searched']
        ProductsQuery = models.Product.objects.filter(Name__contains=searched)
        return render(request, 'miettes/productsearch.html', {'Allproducts': ProductsQuery, 'Query': searched})
    return render(request, 'miettes/productsearch.html')


def discover_view(request, Title):
    discover = models.Discover.objects.get(Title=Title)
    Allproducts = discover.Items.all()
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
            Device = request.session.session_key
            customer, created = models.Customer.objects.get_or_create(
                Device=Device)

        order, created = models.Order.objects.get_or_create(
            Customer=customer, Ordered=False)
        orderitem = models.OrderItem.objects.create(
            Customer=customer, Order=order, Item=Selectedproduct, Color=Color_choice, Size=Size_choice)
        orderitem.save()
        order.save()

    return render(request, 'miettes/viewproduct.html', {'Selectedproduct': Selectedproduct, 'Pictures': Pictures})


def cart_view(request):
    try:
        customer = request.user.Customer
    except:
        Device = request.session.session_key
        customer, created = models.Customer.objects.get_or_create(
            Device=Device)
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
        customer = request.user.Customer
        print("found customer")
    except:
        Device = request.session.session_key
        print(Device)
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
        print(form.is_valid())
        if form.is_valid():
            Address = form.save()
            order.Shipping_address = models.Address.objects.create(
                Country=Address.Country, Street_address=Address.Street_address, Zip=Address.Zip)
            order.Ordered = True
            order.Ordered_date = generate_timestamp() 
            order.Total = total
            order.Customer = customer
            order.save()
            send_html_mail(subject=f"You have received your order {order.Customer.Name}!", html_content=render_to_string(
                'miettes/orderemail.html', {'orderItems': orderitems}), recipient_list=[order.Customer.Email], sender=os.environ.get("EMAIL_HOST_USER_NOREPLY"))
            request.session.flush()
            request.session.cycle_key()

            return render(request, 'miettes/thankyou.html')
    return render(request, 'miettes/checkout.html', {'Order': orderitems, 'form': form, "total": total, "numberofitems": numberofitems})


def thankyou_view(request):
    return render(request, 'miettes/thankyou.html')


def addproduct_view(request):
    form = forms.ProductForm()
    if request.method == 'POST':
        form = forms.ProductForm(request.POST, request.FILES)
        if form.is_valid():
            Product = form.save()


def orderemail_view(request):
    return render(request, 'miettes/orderemail.html')
