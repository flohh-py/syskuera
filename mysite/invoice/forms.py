from django import forms
from django.forms import inlineformset_factory
from .models import Invoice, InvoiceLine


class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = [
                'date',
                'partner',
                'type',
                ]
        widgets = {
                'date': forms.DateInput(attrs={'class': 'form-control container col', 'type': 'date'}),
                'partner': forms.Select(attrs={'class': 'form-control'}),
                'type': forms.Select(attrs={'class': 'form-control'}),
                }


class InvoiceLineForm(forms.ModelForm):
    class Meta:
        model = InvoiceLine
        fields = [
            'parent',
            'item',
            'qty',
            'price'
        ]
        widgets = {
            'parent': forms.HiddenInput(),
        }


InvoiceLineIF = inlineformset_factory(
    Invoice,
    InvoiceLine,
    fields= "__all__",
    form=InvoiceLineForm,
    extra= 1,
)
