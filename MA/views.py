import re
from django.shortcuts import render
from django.db import models
from django.shortcuts import redirect
from . import forms, models
from django.db.models import Q
from string import punctuation
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Case, F, FloatField, Value, When
from django_countries import countries
from django.http import JsonResponse
from miettes.settings import env
from .utils import *
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect
from uuid import uuid4
from django.conf import settings
import requests

def homepage(request):
    Picks = models.Product.objects.filter(Pick=True)
    Collections = models.Collection.objects.filter(Show = True)
    Discover = models.Discover.objects.get(Active = True)

    return render(request, 'miettes/indexdev.html', {'Picks': Picks, 'Collections':Collections, "Discover":Discover})


def aboutus_view(request):
    return render(request, 'miettes/aboutus.html')


def faq_view(request):
    form = forms.CountryForm(initial={'Country': "LB"})
    Zone = models.Country.objects.get(Country="Lebanon")
    response = f'Shipping Cost: {Zone.Zone.Cost}' 
    if request.method == 'POST' and "Country" in request.POST:

            form = forms.CountryForm(request.POST)
            if form.is_valid():
            
                country = dict(countries)[form.cleaned_data['Country']]
                
        
                Zone = models.Country.objects.filter(Country=country)
                if Zone:

                    response = f'Shipping Cost: {Zone[0].Zone.Cost}'
                else:
                    response = "Sorry, we don't ship to your country yet"

                return JsonResponse({"Zone":response}) 
            
    return render(request, 'miettes/faq.html', {'form': form, "Zone": response})

def contactus_view(request):
    if request.method == 'POST' and "contactus" in request.POST:
        # temp_data = {
        # 'response': request.POST.get("g-recaptcha-response"),
        # 'secret': settings.RECAPTCHA_SECRET_KEY
        # }
        # resp = requests.post('https://www.google.com/recaptcha/api/siteverify', data=temp_data)
        # result_json = resp.json()
        # print(result_json)
        # if not result_json.get("success"):
        #     return render(request, 'miettes/contactus.html', {"is_robot":True,'site_key': settings.RECAPTCHA_SITE_KEY})
        # print(result_json)
        email = request.POST.get("email")
        name = request.POST.get("name")
        content = request.POST.get("content")
        models.ContactUs.objects.get_or_create(Name = name, Email = email, Content = content)
        send_html_mail(subject= "Thank you for contacting us", html_content=render_to_string(
            'miettes/contactemail.html'),recipient_list=[email],sender=settings.EMAIL_HOST_USER_SUPPORT,connection=settings.EMAIL_CONNECTIONS["support"])
        send_html_mail(subject= f"{name} sent a contact request", html_content=render_to_string(
            'miettes/supportmail.html',{"email":email,"message":content}),recipient_list=[settings.EMAIL_HOST_USER_SUPPORT],sender=settings.EMAIL_HOST_USER_SUPPORT,connection=settings.EMAIL_CONNECTIONS["support"])
        return render(request, 'miettes/contactus.html',{"sentComplaint": True ,'site_key': settings.RECAPTCHA_SITE_KEY})
    return render(request, 'miettes/contactus.html',{'site_key': settings.RECAPTCHA_SITE_KEY})


def products_view(request):

    categories = models.Category.objects.all()

    GET_params = request.GET.copy()

    filters = {
        'title-ascending': 'Name',
        'title-descending': '-Name',
        'price-ascending': 'Price',
        'price-descending': '-Price',
    }
  
    GET_params.pop('page',0)


    results = models.Product.objects.filter(Status="active")
    results = results.order_by("Status")
    if GET_params.get("Category"):
        results = results.filter(Category__Name=GET_params.get("Category"))
    if GET_params.get("Color"):
        results = results.filter(Color__contains=[GET_params.get("Color")])
    if GET_params.get("sort_by"):
        results = results.order_by(filters[GET_params.get("sort_by")])

    



    paginator = Paginator(results, 24)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'miettes/productsdev.html', {'page_obj': page_obj,"GET_params":GET_params, "categories":categories})






def initial_query(queryInput):
    return Q(Name__icontains=queryInput)|Q(SKU=queryInput)|Q(Description__icontains=queryInput)|Q(Category__icontains=queryInput)


def query(inpt):
    return models.Product.objects.annotate(
        k1=Case(
            When(Name__icontains=inpt, then=Value(2.0)),
            default=Value(0.0),
            output_field=FloatField(),
        ),
        k2=Case(
            When(SKU=inpt, then=Value(10.0)),
            default=Value(0.0),
            output_field=FloatField(),
        ),
        k3=Case(
            When(Description__icontains=inpt, then=Value(1.0)),
            default=Value(0.0),
            output_field=FloatField(),
        ),
        k4=Case(
            When(Category__Name__contains=inpt, then=Value(1.0)),
            default=Value(0.0),
            output_field=FloatField(),
        ),
        rank=F("k1") + F("k2") + F("k3") + F("k4"),
    ).order_by("-rank").exclude(rank=0.0)


def search_view(request):
    queryInput = request.GET.get("q").strip().strip(punctuation)
    results = query(queryInput)
        
    paginator = Paginator(results, 24)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    return render(request, 'miettes/search.html',{"queryInput":queryInput, "page_obj":page_obj})


def discover_view(request):
    discover = models.Discover.objects.get(Active=True)
    results = models.Product.objects.filter(Discover = discover)
    paginator = Paginator(results, 24)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'miettes/collections.html', {'page_obj': page_obj,"collection":discover})


def collection_view(request, Title_en):
    collection = models.Collection.objects.get(Title_en=Title_en)
    results = models.Product.objects.filter(Collection = collection)

    paginator = Paginator(results, 24)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number) 
    return render(request, 'miettes/collections.html', {'page_obj': page_obj, "collection":collection})





def viewproduct_view(request, SKU):
    Selectedproduct = models.Product.objects.filter(SKU=SKU)[0]
    numOfPictures = 1
    Pictures = models.Picture.objects.filter(Product=Selectedproduct)
    if not Pictures.exists():
        Pictures = models.Picture.objects.none()
    numOfPictures+=Pictures.count()

    if request.method == "POST" and "addtocart" in request.POST:
        Color_choice = ""
        Size_choice = ""
        Color_choices = request.POST.getlist("color")
        if Color_choices:
            Color_choice = Color_choices[0]
        Size_choices = request.POST.getlist("size")
        if Size_choices:
            Size_choice = Size_choices[0]

    
        if not request.session.get("sess"):
            request.session["sess"] = str(uuid4()) 
   
        Device = request.session.get("sess")
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
    context = {'Selectedproduct': Selectedproduct, 'Pictures': Pictures,"Colors":colors,"ColorsMobile":colorsMobile,"numOfPictures":range(numOfPictures)}
    if numOfPictures <= 1:
        del context["numOfPictures"]
    return render(request, 'miettes/viewproductdev.html',context)


def cart_view(request):
    sent = False

    if not request.session.get("sess"):
            request.session["sess"] = str(uuid4()) 
   
    Device = request.session.get("sess")


    customer, created = models.Customer.objects.get_or_create(
            Device=Device)
       
    order, created = models.Order.objects.get_or_create(
        Customer=customer, Ordered=False)
    orderitems = models.OrderItem.objects.filter(Order=order.pk)
    total, numberofitems = get_total_and_items(orderitems)
    if request.method == 'POST' and "contact[email]" in request.POST:
            sent = True
            email = request.POST.get("contact[email]")
            object, created = models.Newsletter.objects.get_or_create(Email=email)
            if created:
                send_html_mail(subject= " Thank you for subscribing!", html_content=render_to_string(
            'miettes/newslettersubscription.html'),recipient_list=[email],sender=settings.EMAIL_HOST_USER_NEWSLETTER,connection=settings.EMAIL_CONNECTIONS["newsletter"])
            sent = created
    if request.method=="POST" and "length" in request.POST:
        length = request.POST.get("length")

        if numberofitems==int(length):
            difference = False
        else:
            difference = True
            messages.success(request, "Item added to cart")
     
        
        return JsonResponse({"Difference":difference})
    
    


    return {'Order': orderitems, "total": total, "numberofitems": numberofitems,"numOfItems":len(orderitems),"sent":sent}

def checkcart_view(request):
    if not request.session.get("sess"):
            request.session["sess"] = str(uuid4()) 
   
    Device = request.session.get("sess")


    customer, created = models.Customer.objects.get_or_create(
            Device=Device)
       
    order, created = models.Order.objects.get_or_create(
        Customer=customer, Ordered=False)
    orderitems = models.OrderItem.objects.filter(Order=order.pk)
    length = request.POST.get("length") 
    total, numberofitems = get_total_and_items(orderitems)
    


def navbar_view(request):
    categories = models.Category.objects.all()
    collections = models.Collection.objects.filter(Show = True)
    return {'categories': categories, 'collections': collections}

def removeitem_view(request, orderItemID):
    orderItem = models.OrderItem.objects.filter(id=int(orderItemID)).first()
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

      
 
    if not request.session.get("sess"):
            request.session["sess"] = str(uuid4()) 
   
    Device = request.session.get("sess")
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
        customer.First_name = First_name 
        customer.Last_name = Last_name
        customer.Email = Email
        
        if form.is_valid():
            Address = form.save()
            if models.Country.objects.filter(Country=Address.Country.name).first():
                order.Shipping_address = models.Address.objects.create(City = Address.City,
                    Country=Address.Country, Street_address=Address.Street_address, Zip=Address.Zip,Phone_number = Address.Phone_number)
                customer.Phone_number=Address.Phone_number
                order.Additional_comments=request.POST.get("comments")
                customer.save()
                order.save()

                return redirect("payment")
            
    return render(request, 'miettes/checkout.html', {'Order': orderitems, 'form': form, "total": total, "numberofitems": numberofitems})


def get_shipping_cost(order):
    country = order.Shipping_address.Country.name

    countryZone = models.Country.objects.get(Country = country)
    return countryZone.Zone



def payment_view(request):
    if not request.session.get("sess"):
            request.session["sess"] = str(uuid4()) 
   
    Device = request.session.get("sess")
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
        ImagesEmail = [switch_extension(image.Item.Image.url)[1:] for image in orderitems]
        orderItems = [item for item in orderitems]
   
        zippedOrder = zip(ImagesEmail,orderItems)
        send_html_mail(subject=f"Order completed {order.Ref_code}!", html_content=render_to_string(
            'miettes/orderemail.html', {"total":order.Total,"subtotal":order.Subtotal,"shipping":order.Shipping,'zippedOrder': zippedOrder,'orderNumber':order.Ref_code,'address':order.Shipping_address}), recipient_list=[order.Customer.Email], sender=settings.EMAIL_HOST_USER_NOREPLY,Images=Images)
        send_html_mail(subject=f"New Order {order.Ref_code}", html_content=render_to_string(
            'miettes/neworder.html', {"total":order.Total,'orderNumber':order.Ref_code,"Customer":order.Customer,"Ordered_date":order.Ordered_date,"orderitems":orderitems}), recipient_list=[settings.EMAIL_HOST_USER_NOREPLY], sender=settings.EMAIL_HOST_USER_NOREPLY)
        if request.session.get("sess"):
            del request.session["sess"]
        request.session["sess"] = str(uuid4())

        return render(request, 'miettes/thankyou.html',{"orderNumber":order.Ref_code})

    return render(request,"miettes/payment.html",{'Customer':customer,"Comments":order.Additional_comments,"Address":order.Shipping_address,"Zone":shippingZone,"subtotal":subtotal,"total":shippingZone.Cost+subtotal})
    


def webmail_view(request):
    return redirect("https://www.zoho.com/mail/login.html")



#_________________Error handler______________________________






def page_not_found_view(request,exception):
    return render(request,"miettes/404.html",status=404)

def internal_server_error_view(request,exception=None):
    return render(request,"miettes/500.html",status=500)

def permission_denied_view(request,exception=None):
    return render(request,"miettes/403.html",status=403)

def bad_request_view(request,exception=None):
    return render(request,"miettes/400.html",status=400)