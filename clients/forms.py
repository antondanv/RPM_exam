from django import forms

from .models import Client


class ClientForm(forms.ModelForm):
    registration_date = forms.DateField(
        input_formats=['%Y-%m-%d'],
        widget=forms.DateInput(
            attrs={'class': 'form-control', 'type': 'date'},
            format='%Y-%m-%d',
        ),
        label='Дата регистрации',
    )

    class Meta:
        model = Client
        fields = ['full_name', 'email', 'phone', 'registration_date']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
        }
