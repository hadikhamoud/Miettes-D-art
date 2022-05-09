from django.db import models
from django.contrib.auth.models import User
from datetime import datetime,timedelta,timezone
from django_countries.fields import CountryField
from django.conf import settings
from django.contrib.postgres.fields import ArrayField
import uuid
from shortuuidfield import ShortUUIDField
import random
import string
from djmoney.models.fields import MoneyField
from phonenumber_field.modelfields import PhoneNumberField

def generate_Ref_code():
    current_date =datetime.now()
    Ref_code = str(int(current_date.strftime("%y%m%d")))+''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(4))
    return Ref_code


def ConvertCheck():
    multiplier = models.Convert.objects.all()
    return multiplier[0]


def get_default_size():
    return ['XS','S','M','L','XL']
def get_default_color():
    return ['Gold', 'Silver']




class Product(models.Model):
    catchoice= [
        ('earrings', 'Earrings'),
        ('objet dart', "objet d'art"),
        ('rings', 'Rings'),
        ('necklaces', 'Necklaces'),
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
    Size = ArrayField(models.CharField(max_length=10,null = True, blank=True),null = True, blank=True,default = get_default_size)
    Color = ArrayField(models.CharField(max_length=10,null = True, blank=True),null = True, blank=True,default = get_default_color)
    Description = models.CharField(max_length=400,null = True, blank=True)
    Price = MoneyField(max_digits=14, decimal_places=2, default_currency='USD',null = True, blank = True)
    Category = models.CharField(max_length=30,choices=catchoice,default='earrings',null = True, blank=True)
    Status = models.CharField(max_length=30,choices=statuschoice,default='Active',null = True, blank=True)
    Optional = models.CharField(max_length=30,choices=optionalchoice,default='new arrivals',null = True, blank=True)
    Discover = models.ForeignKey('Discover',on_delete=models.CASCADE,null = True, blank = True)
    Image = models.ImageField(upload_to='static/images',null = True, blank=True)
    PriceLBP = MoneyField(max_digits=14, decimal_places=2, default_currency='USD',null = True, blank = True)


    def __str__(self):
        return self.Name+" "+self.SKU


class Multiplier(models.Model):
     USDtoLBP = models.IntegerField(default=14000)

     def __str__(self):
         return "set Rate to: " + str(self.USDtoLBP)



class Picture(models.Model):
    Product = models.ForeignKey('Product',on_delete=models.CASCADE,null = True, blank = True)
    picture = models.ImageField(upload_to='static/images')


class Customer(models.Model):
    User = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE,editable=False)
    Name = models.CharField(max_length=200, null=True, blank=True,editable=False)
    Email = models.EmailField(max_length=254,null=True, blank=True,editable=False)
    Device = models.CharField(max_length=200, null=True, blank=True,editable=False)
    Phone_number = PhoneNumberField(max_length=200,null=True, blank=True,editable=False)



    def __str__(self):
        if self.Name:
            name = self.Name
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
        return f"{self.Item.Name} ------ {self.Size} ----- {self.Color}"

    def get_total_item_price(self):
        return self.Quantity * self.Item.Price




class Order(models.Model):

    Customer = models.ForeignKey('Customer',
                             on_delete=models.CASCADE,null = True, blank = True)
    #Ref_code = models.UUIDField(default=uuid.uuid4, unique=True, db_index=True, editable=False)
    Ref_code = ShortUUIDField()

    #Items = models.ManyToManyField(OrderItem)
    Start_date = models.DateTimeField(auto_now=True,null = True)
    Ordered_date = models.DateTimeField(blank=True, null=True)
    Ordered = models.BooleanField(default=False)
    Shipping_address = models.OneToOneField(
        'Address', on_delete=models.SET_NULL, blank=True, null=True)
    Total = MoneyField(max_digits=14, decimal_places=2, default_currency='USD',null = True, blank = True)
    Being_delivered = models.BooleanField(default=False)
    Received = models.BooleanField(default=False)

    class Meta:
        ordering=['-Ordered']

    def __str__(self):
        return str(self.Customer) + str(self.Ref_code)





class Discover(models.Model):
    Title = models.CharField(max_length=40,null = True, blank=True)
    Image1 = models.ImageField(upload_to='static/images',null = True, blank=True)
    Image2 =  models.ImageField(upload_to='static/images',null = True, blank=True)
    Image3 =  models.ImageField(upload_to='static/images',null = True, blank=True)
    Items = models.ManyToManyField(Product)



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
