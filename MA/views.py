from django.shortcuts import render
from django.db import models
from django.shortcuts import render
from django.http import HttpResponseRedirect
from . import forms,models
from django.http import HttpResponseRedirect
from django.contrib.auth.models import Group
from django.contrib import auth
from django.contrib.auth.decorators import login_required,user_passes_test


# Create your views here.
def homepage(request):
    return render(request,'miettes/index.html')


def aboutus_view(request):
    return render(request,'miettes/aboutus.html')



def contactus_view(request):
    return render(request,'miettes/contactus.html')


def products_view(request):
    Allproducts = models.Product.objects.all()
    return render(request,'miettes/products.html',{'Allproducts': Allproducts})


def viewproduct_view(request, SKU):
    Selectedproduct = models.Product.objects.filter(SKU = SKU)[0]
    return render(request,'miettes/viewproduct.html',{'Selectedproduct': Selectedproduct})



def addproduct_view(request):
    form=forms.ProductForm()
    if request.method=='POST':
        form=forms.ProductForm(request.POST,request.FILES)
        if form.is_valid():
            Product = form.save()
    return render(request,'miettes/addproduct.html',{'form':form})
