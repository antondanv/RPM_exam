from django import forms
from .models import Product

class ProductFrom(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'price', 'sku']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'sku': forms.TextInput(attrs={'class': 'form-control'})
        }