from email.policy import default
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django_countries.fields import CountryField
from django.conf import settings
from django.contrib.postgres.fields import ArrayField

from djmoney.models.fields import MoneyField
from phonenumber_field.modelfields import PhoneNumberField
# from django.core.validators import MaxLengthValidator
from .utils import *
import os
from colorfield.fields import ColorField
import string

from django.template.loader import render_to_string
from django_resized import ResizedImageField




def ConvertCheck():
    multiplier = models.Convert.objects.all()
    return multiplier[0]





class Product(models.Model):
    catchoice= [
        ('earrings', 'earrings'),
        ('objet dart', "objet d'art"),
        ('rings', 'rings'),
        ('necklaces', 'necklaces'),
        ]
    statuschoice= [
        ('active', 'Active'),
        ('disabled', 'Disabled'),
        ]
    optionalchoice= [
        ('best seller', 'Best Seller'),
        ('new arrivals', 'New Arrivals'),
        ('on sale', 'On Sale')
        ]
    sizechoice= [
            ('XS', 'XS'),
            ('S', 'S'),
            ('M', 'M'),
            ('L', 'L'),
            ('XL', 'XL')
            ]
    sizedefault = ['XS','S','M','L','XL']
    colordefault = ['Gold', 'Silver']


    Name = models.CharField(max_length=40,null = True, blank=True)
    SKU = models.CharField(max_length=40,unique = True)
    Pick=models.BooleanField(default=False)
    Size = ArrayField(models.CharField(max_length=10,null = True, blank=True),null = True, blank=True,default = get_default_size)
    Color = ArrayField(models.CharField(max_length=30,null=True,blank=True),null = True, blank=True,default = get_default_color)
    ColorHex = ArrayField(models.CharField(max_length=30,null=True,blank=True),null = True, blank=True,default = get_default_color)
    Description = models.TextField(max_length=400,null = True, blank=True)
    Price = MoneyField(max_digits=14, decimal_places=2, default_currency='USD',null = True, blank = True)
    Category = models.CharField(max_length=30,choices=catchoice,default='earrings',null = True, blank=True)
    Status = models.CharField(max_length=30,choices=statuschoice,default='active',null = True, blank=True)
    Optional = models.CharField(max_length=30,choices=optionalchoice,default='new arrivals',null = True, blank=True)
    Discover = models.ForeignKey('Discover',on_delete=models.CASCADE,null = True, blank = True)
    Collection = models.ForeignKey('Collection',on_delete=models.CASCADE,null = True, blank = True)
    Image = models.ImageField(upload_to='static/images',null = True, blank=True)
    PriceLBP = MoneyField(max_digits=14, decimal_places=2, default_currency='LBP',null = True, blank = True)


    def __str__(self):
        try:
            return self.Name+" "+self.SKU
        except:
            return ""
    

    def delete(self):
        self.Status = "disabled"
        super(Product, self).save()
      


class Color(models.Model):
    colorHex = models.CharField(max_length=7,unique = True)
    colorName = models.CharField(max_length=20)

    def __str__(self):
        return self.colorName
    


class Multiplier(models.Model):
     USDtoLBP = models.IntegerField(default=14000)

     def __str__(self):
         return "set Rate to: " + str(self.USDtoLBP)



class Picture(models.Model):
    Product = models.ForeignKey('Product',on_delete=models.CASCADE,null = True, blank = True)
    picture = ResizedImageField(force_format="WebP",quality=83, upload_to='static/images',null=True,blank=True)


class Customer(models.Model):
    User = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE,editable=False)
    First_name = models.CharField(max_length=200, null=True, blank=True,editable=False)
    Last_name = models.CharField(max_length=200, null=True, blank=True,editable=False)
    Email = models.EmailField(max_length=254,null=True, blank=True,editable=False)
    Device = models.CharField(max_length=200, null=True, blank=True,editable=False)
    Phone_number = PhoneNumberField(max_length=200,null=True, blank=True,editable=False)



    def __str__(self):
        if self.First_name and self.Last_name:
            name  = f'{self.First_name} {self.Last_name}'

        else:
            name = self.Device
        return str(name)




class OrderItem(models.Model):
    Customer = models.ForeignKey('Customer',
                             on_delete=models.SET_NULL,null = True, blank = True)
    Done = models.BooleanField(default=False)
    Order = models.ForeignKey('Order', on_delete=models.CASCADE,null = True, blank = True)
    Item = models.ForeignKey('Product', on_delete=models.CASCADE)
    Color = models.CharField(max_length=40,null = True, blank=True)
    Size = models.CharField(max_length=40,null = True, blank=True)
    Quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.Item.Name} \t- {self.Size} \t- {self.Color}"

    def get_total_item_price(self):
        return self.Quantity * self.Item.Price




class Order(models.Model):

    Customer = models.ForeignKey('Customer',
                             on_delete=models.CASCADE,null = True, blank = True)
    #Ref_code = models.UUIDField(default=uuid.uuid4, unique=True, db_index=True, editable=False)
    Ref_code = models.CharField(max_length=12,null=True, blank=True, unique=True)


    #Items = models.ManyToManyField(OrderItem)
    Start_date = models.DateTimeField(auto_now=True,null = True)
    Ordered_date = models.DateTimeField(blank=True, null=True)
    Shipped_date = models.DateTimeField(blank=True, null=True)
    Delivered_date = models.DateTimeField(blank=True, null=True)
    Ordered = models.BooleanField(default=False)
    Shipping_address = models.OneToOneField(
        'Address', on_delete=models.SET_NULL, blank=True, null=True)
    Subtotal = MoneyField(max_digits=14, decimal_places=2, default_currency='USD',null = True, blank = True)
    Shipping = MoneyField(max_digits=14, decimal_places=2, default_currency='USD',null = True, blank = True)
    Total = MoneyField(max_digits=14, decimal_places=2, default_currency='USD',null = True, blank = True)
    Shipped = models.BooleanField(default=False)
    Delivered = models.BooleanField(default=False)

    class Meta:
        ordering=['-Ordered']

    def __str__(self):
        return str(self.Customer) +" "+ str(self.Ref_code)

    
    def save(self, *args, **kwargs):

        if not self.Ref_code:
            self.Ref_code = generate_Ref_code()
            while Order.objects.filter(Ref_code=self.Ref_code).exists():
                self.Ref_code = generate_Ref_code()
        

        #admin should press shipped then delivered(in that order)
        if self.Shipped and not self.Delivered:
            print("shipped")
            send_html_mail(subject = "Your order is on its way", html_content=render_to_string(
            'miettes/shippedemail.html', {'orderNumber':self.Ref_code,'address':self.Shipping_address}), recipient_list=[self.Customer.Email], sender=os.environ.get("EMAIL_HOST_USER_NOREPLY"))
            self.Shipped_date = generate_timestamp() 
        elif self.Shipped and self.Delivered: 
            print("delivered")
            send_html_mail(subject = "Order delivered", html_content=render_to_string(
            'miettes/shippedemail.html', {'orderNumber':self.Ref_code,'address':self.Shipping_address}), recipient_list=[self.Customer.Email], sender=os.environ.get("EMAIL_HOST_USER_NOREPLY"))
            self.Delivered_date = generate_timestamp()


        super(Order, self).save(*args, **kwargs)





class Discover(models.Model):
    Title = models.CharField(max_length=80,null = True, blank=True)
    Image = ResizedImageField(force_format="WebP",quality=83, upload_to='static/images',null=True,blank=True)
    Description = models.TextField(null = True, blank = True)
    Active = models.BooleanField(default = False)
    Items = models.ManyToManyField(Product)



    def __str__(self):
        return self.Title
    

    def save(self, *args, **kwargs):
        if self.Active:
            Discover.objects.all().update(Active = False)
            self.Active = True
        super(Discover, self).save(*args, **kwargs)
 
        



class Collection(models.Model):
    Title = models.CharField(max_length=80,null = True, blank=True)
    Title_en = models.CharField(max_length=80,null = True, blank=True)
    Description = models.TextField(null = True, blank = True)
    Image =ResizedImageField(force_format="WebP",quality=83, upload_to='static/images',null=True,blank=True)
    Items = models.ManyToManyField(Product)
    Show = models.BooleanField(default = False)

    def save(self, *args, **kwargs):
        self.Title_en = self.Title.replace(" ","-").lower()
        # self.Title_en = self.Title
        self.Title_en = self.Title_en.strip(string.punctuation)
        super(Collection, self).save(*args, **kwargs)


    def __str__(self):
        return self.Title




class Address(models.Model):
    # Customer = models.ForeignKey('Customer',
    #                          on_delete=models.SET_NULL,null = True, blank = True)
    Street_address = models.CharField(max_length=100,null = True, blank = True)
    Apartment_address = models.CharField(max_length=100,null = True, blank = True)
    City = models.CharField(max_length=100,null = True, blank = True)
    Country = CountryField(multiple=False)
    Zip = models.CharField(max_length=100,null = True, blank = True)
    Phone_number = PhoneNumberField(max_length=200,null=True, blank=True)
    Default = models.BooleanField(default=False,null = True, blank = True)

    def __str__(self):
        return self.Street_address+ '\n' +self.Zip + '\n' + str(self.Country) + '\n' + 'Phone Number: ' + str(self.Phone_number)

    class Meta:
        verbose_name_plural = 'Addresses'





class ContactUs(models.Model):
    Name = models.CharField(max_length=200, null=True, blank=True,editable=False)
    Email = models.EmailField(max_length=254,null=True, blank=True,editable=False)
    Content = models.TextField(null = True, blank=True)
    Response = models.TextField(null = True, blank = True)



    def __str__(self):
        return f"{str(self.Name)} : {str(self.Email)}"

    
    def save(self, *args, **kwargs):

        if self.Response:
            send_html_mail("Support!",f"<h1> we have received your complaint!<br></br> {self.Response}</h1>", recipient_list=[self.Email],sender=os.environ.get("EMAIL_HOST_USER_SUPPORT"))

        super(ContactUs, self).save(*args, **kwargs)
    
    class Meta:
        # Add verbose name
        verbose_name = 'Contact Us'
        verbose_name_plural= "Contact Us"
        



class Zone(models.Model):
    ZoneNumber = models.IntegerField(null=True,blank=True)
    Cost = MoneyField(max_digits=14, decimal_places=2, default_currency='USD',null = True, blank = True)

    def __str__(self):
        return "Zone " + str(self.ZoneNumber)


class Country(models.Model):
    Country = models.CharField(max_length=120,null=True,blank=True)
    Zone = models.ForeignKey("Zone",null=True,blank=True,on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Country'
        verbose_name_plural = 'Countries'

    def __str__(self):
        return str(self.Country)



class Newsletter(models.Model):
    Email = models.EmailField(max_length=254,null=True, blank=True)
    Name = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.Email

    class Meta:
        verbose_name = 'Newsletter'
        verbose_name_plural = 'Newsletters'