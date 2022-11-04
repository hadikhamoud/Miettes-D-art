from django import forms
from django.contrib.auth.models import User
from . import models
from django.forms.widgets import TextInput


class ProductForm(forms.ModelForm):
    class Meta:
        model = models.Product
        exclude=[]
        widgets = {
        'Description':forms.Textarea(attrs={'rows': 3, 'cols': 30})
        }


class AddressForm(forms.ModelForm):
    
    class Meta:
        model = models.Address
        exclude=['Customer','Apartment_address','Default']

    


# class ProductForm(forms.ModelForm):
#     class Meta:
#         model = models.Product
#         fields = '__all__'
#         widgets = {
#             'Color': TextInput(attrs={'type': 'Color'}),
#         }