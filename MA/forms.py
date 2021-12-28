from django import forms
from django.contrib.auth.models import User
from . import models


class ProductForm(forms.ModelForm):
    class Meta:
        model = models.Product
        exclude=[]
