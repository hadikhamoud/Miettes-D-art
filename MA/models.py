from django.db import models
from django.contrib.auth.models import User
from datetime import datetime,timedelta,timezone




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

    Name = models.CharField(max_length=40,null = True, blank=True)
    SKU = models.CharField(max_length=40,unique = True)
    Size = models.CharField(max_length=40,null = True, blank=True)
    Color = models.CharField(max_length=40,null = True, blank=True)
    Category = models.CharField(max_length=40,null = True, blank=True)
    Description = models.CharField(max_length=40,null = True, blank=True)
    Price = models.FloatField(null = True, blank=True)
    Category = models.CharField(max_length=30,choices=catchoice,default='earrings',null = True, blank=True)
    Status = models.CharField(max_length=30,choices=statuschoice,default='Active',null = True, blank=True)
    Optional = models.CharField(max_length=30,choices=optionalchoice,default='new arrivals',null = True, blank=True)
    Image = models.ImageField(upload_to='static/images',null = True, blank=True)

    def __str__(self):
        return self.Name+" "+self.SKU


class Cart(models.Model):
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=datetime.now)


class CartItem(models.Model):
    Product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.FloatField(blank=True)
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE)

    def price_total(self):
        return self.price*self.quantity



class Order(models.Model):

    Customer=models.ForeignKey(User,on_delete=models.CASCADE)
    Item = models.OneToOneField('Product',on_delete=models.CASCADE)
    Comment = models.CharField(max_length=40)
    OrderNumber = models.IntegerField(unique = True)

    def __str__(self):
        return self.Customer.first_name+" "+self.Customer.last_name+" order number: " + ' ['+str(self.OrderNumber)+']'
    @property
    def get_name(self):
        return self.Customer.first_name
    @property
    def getuserid(self):
        return self.Customer.id
