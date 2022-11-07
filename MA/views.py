import re
from django.shortcuts import render
from django.db import models
from django.shortcuts import redirect
from phonenumbers import PhoneNumber
from . import forms, models
from django.db.models import Q
from string import punctuation
from django.core.paginator import Paginator
from django.contrib import messages

from django.template import RequestContext


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
from django.http import HttpResponseRedirect
from bs4 import BeautifulSoup as bsoup
# Create your views here.

def mainScraper():
    productsDir = os.listdir("/Users/hadihamoud/Desktop/Personal work/Miettes_General_Scraper/Products_HTML_Pages")
    for i in range(len(productsDir)):
        print("heree")
        try:
            with open(os.path.join("/Users/hadihamoud/Desktop/Personal work/Miettes_General_Scraper/Products_HTML_Pages",productsDir[i]), 'r') as f:
        # with open(dir, 'r') as f:
            
                contents = f.read()

                reader = bsoup(contents,"lxml")
                
                # print(extract_images(reader))
                # print(extract_title(reader))
                # print(extract_category(reader))
                # print(extract_price(reader))
                # print(extract_status(reader))
                # print(extract_SKU(reader))
                # print(extract_description(reader))

                models.Product.objects.create(SKU = extract_SKU(reader), Name = extract_title(reader), Description = extract_description(reader), Category = extract_category(reader), Price = extract_price(reader), Status = extract_status(reader),Image="static/images/discover.jpeg")
                print("here")
        
        except Exception as e:
            print(e)



def homepage(request):
    # mainScraper()
    Picks = models.Product.objects.filter(Pick=True)
    Collections = models.Collection.objects.filter(Show = True)
    Discover = models.Discover.objects.filter(Active = True)[0]

    if request.method == 'POST':
        email = request.POST.get("contact[email]")
        email = models.Newsletter.objects.get_or_create(Email=email)
        return render(request, 'miettes/indexdev.html', {"Picks": Picks, "Collections": Collections, "Discover": Discover, "sent": True})

    return render(request, 'miettes/indexdev.html', {'Picks': Picks, 'Collections':Collections, "Discover":Discover})


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


def clean_filters(filters):
    filters = {k: v for k, v in filters.items() if v}
    return filters

def products_view(request):

    GET_params = request.GET.copy()
    print(GET_params)

    if GET_params.get("page"):
        del GET_params['page']




    results = models.Product.objects.filter(Status="active")
    if GET_params.get("Category"):
        results = results.filter(Category=GET_params.get("Category"))
    if GET_params.get("Color"):
        results = results.filter(Color__contains=[GET_params.get("Color")])
    if GET_params.get("sort_by") == "price-ascending":
        results = results.order_by("Price")
    elif GET_params.get("sort_by") == "price-descending":
        results = results.order_by("-Price")
    elif GET_params.get("sort_by") == "title-ascending":
        results = results.order_by("Name")
    elif GET_params.get("sort_by") == "title-descending":
        results = results.order_by("-Name")
    



    paginator = Paginator(results, 24)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'miettes/productsdev.html', {'page_obj': page_obj,"GET_params":GET_params})




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




def search_view(request):
    queryInput = request.GET.get("q").strip().strip(punctuation)
    print(queryInput)
    fullQuery = Q(Name__icontains=queryInput)|Q(SKU=queryInput)|Q(Description__icontains=queryInput)|Q(Category__icontains=queryInput)
    results = models.Product.objects.filter(fullQuery).filter(Status="active")
        
    paginator = Paginator(results, 24)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    print(page_obj)

    return render(request, 'miettes/search.html',{"Allproducts":results,"queryInput":queryInput, "page_obj":page_obj})


def discover_view(request, Title):
    discover = models.Discover.objects.get(Title=Title)
    Allproducts = discover.Items.all()
    return render(request, 'miettes/discover.html', {'Allproducts': Allproducts})


def collection_view(request, Title):
    collection = models.Collection.objects.get(Title=Title)
    results = models.Product.objects.filter(Collection = collection)
    paginator = Paginator(results, 24)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number) 
    return render(request, 'miettes/collections.html', {'page_obj': page_obj})




def viewproduct_view(request, SKU):
    Selectedproduct = models.Product.objects.filter(SKU=SKU)[0]
    Pictures = models.Picture.objects.filter(Product=Selectedproduct)
    print(Selectedproduct.collection_set.all())
    if not Pictures.exists():
        Pictures = models.Picture.objects.none()

    if request.method == "POST":
        Color_choice = request.POST.getlist("color")[0]
        Size_choice = request.POST.getlist("size")[0]

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
        messages.success(request, "Item added to cart")
        return HttpResponseRedirect(f'/viewproduct/{SKU}')
    
    colors = zip(Selectedproduct.Color,Selectedproduct.ColorHex)
    colorsMobile = zip(Selectedproduct.Color,Selectedproduct.ColorHex)
    return render(request, 'miettes/viewproductdev.html', {'Selectedproduct': Selectedproduct, 'Pictures': Pictures,"Colors":colors,"ColorsMobile":colorsMobile})


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

    return {'Order': orderitems, "total": total, "numberofitems": numberofitems,"numOfItems":len(orderitems)}


def removeitem_view(request, orderItemID):
    orderItem = models.OrderItem.objects.get(id=int(orderItemID))
    if orderItem:
        orderItem.delete()
        messages.success(request, "Item removed from cart")
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


def clearcart_view(request):
    orderItem = models.OrderItem.objects.filter(Customer=request.user.customer)
    for item in orderItem:
        item.delete()
    messages.success(request, "cart cleared")
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


def checkout_view(request):
    try:
        customer = request.user.Customer
    except:
        Device = request.session.session_key
        customer, created = models.Customer.objects.get_or_create(
            Device=Device)
    
    order, created = models.Order.objects.get_or_create(
        Customer=customer, Ordered=False)
    orderitems = models.OrderItem.objects.filter(Order=order.pk)


    if not orderitems:
        return redirect("/")
    
    
    form = forms.AddressForm(initial={'Country': 'LB'})



    
    total, numberofitems = get_total_and_items(orderitems)
    if request.method == "POST":
        form = forms.AddressForm(request.POST)
        First_name = request.POST.get("fname")
        Last_name = request.POST.get("lname")
        Email = request.POST.get("email")
        customer.Name = f'{First_name} {Last_name}'
        customer.Email = Email
        
        if form.is_valid():
            Address = form.save()
            order.Shipping_address = models.Address.objects.create(City = Address.City,
                Country=Address.Country, Street_address=Address.Street_address, Zip=Address.Zip,Phone_number = Address.Phone_number)
            #TODO add Customer.phonenumber and assign it using input
            customer.Phone_number=Address.Phone_number
            customer.save()
            order.save()
            print(order.Shipping_address.Country.name)
            return redirect("payment")
            
    return render(request, 'miettes/checkout.html', {'Order': orderitems, 'form': form, "total": total, "numberofitems": numberofitems})


def get_shipping_cost(order):
    country = order.Shipping_address.Country.name
    # if country=="Lebanon":
    #     return 
    countryZone = models.Country.objects.get(Country = country)
    return countryZone.Zone



def payment_view(request):
    Device = request.session.session_key
    customer, created = models.Customer.objects.get_or_create(
            Device=Device)
    
    order, created = models.Order.objects.get_or_create(
        Customer=customer, Ordered=False)
    orderitems = models.OrderItem.objects.filter(Order=order.pk)
    
    if not orderitems:
        return redirect("/")
    if not order.Shipping_address:
        return redirect("checkout")

    subtotal, numberofitems = get_total_and_items(orderitems)

    shippingZone = get_shipping_cost(order)

 
    if request.method == 'POST':

        order.Ordered = True
        order.Ordered_date = generate_timestamp() 
        order.Subtotal = subtotal
        order.Shipping = shippingZone.Cost
        order.Total = subtotal + shippingZone.Cost
        order.Customer = customer
        order.save()
        Images = [image.Item.Image.url for image in orderitems]
     
        send_html_mail(subject=f"Order completed {order.Ref_code}!", html_content=render_to_string(
            'miettes/orderemail.html', {"total":order.Total,"subtotal":order.Subtotal,"shipping":order.Shipping,'orderItems': orderitems,'orderNumber':order.Ref_code,'address':order.Shipping_address}), recipient_list=[order.Customer.Email], sender=os.environ.get("EMAIL_HOST_USER_NOREPLY"),Images=Images)
        request.session.flush()
        request.session.cycle_key()

        return render(request, 'miettes/thankyou.html',{"orderNumber":order.Ref_code})

    return render(request,"miettes/payment.html",{'Customer':customer,"Address":order.Shipping_address,"Zone":shippingZone,"subtotal":subtotal,"total":shippingZone.Cost+subtotal})
    

# def thankyou_view(request):
#     try:
#         customer = request.user.Customer
#     except:
#         Device = request.session.session_key
#         customer, created = models.Customer.objects.get_or_create(
#             Device=Device)
    
#     order, created = models.Order.objects.get_or_create(
#         Customer=customer, Ordered=False)
#     return render(request, 'miettes/thankyou.html',{"orderNumber":order.Ref_code})


def addproduct_view(request):
    form = forms.ProductForm()
    if request.method == 'POST':
        form = forms.ProductForm(request.POST, request.FILES)
        if form.is_valid():
            Product = form.save()


def orderemail_view(request):
    return render(request, 'miettes/orderemail.html')




#_________________Error handler______________________________






def page_not_found_view(request,exception):
    return render(request,"miettes/404.html",status=404)
