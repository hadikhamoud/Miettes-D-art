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

    
class CollectionForm(forms.ModelForm):
    class Meta:
        model = models.Collection
        fields=['Title','Description','Image',"Show","Title_en"]
        exclude=['Items']


    products = forms.ModelMultipleChoiceField(queryset=models.Product.objects.all())

    def __init__(self, *args, **kwargs):
        super(CollectionForm, self).__init__(*args, **kwargs)
        if self.instance:
            self.fields['products'].initial = self.instance.product_set.all()

    def save(self, *args, **kwargs):
 
        instance = super(CollectionForm, self).save(commit=False)
        self.fields['products'].initial.update(Collection=None)
        self.cleaned_data['products'].update(Collection=instance)
        return instance



class DiscoverForm(forms.ModelForm):
    class Meta:
        model = models.Discover
        fields=['Title','Description','Image',"Active"]
        exclude=['Items']


    products = forms.ModelMultipleChoiceField(queryset=models.Product.objects.all())

    def __init__(self, *args, **kwargs):
        super(DiscoverForm, self).__init__(*args, **kwargs)
        if self.instance:
            self.fields['products'].initial = self.instance.product_set.all()

    def save(self, *args, **kwargs):
 
        instance = super(DiscoverForm, self).save(commit=False)
        self.fields['products'].initial.update(Discover=None)
        self.cleaned_data['products'].update(Discover=instance)
        return instance
