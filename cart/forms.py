from django import forms

CHOICES = [(i, str(i)) for i in range(1, 6)]


class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=CHOICES, coerce=int)
    override = forms.BooleanField(required=False, widget=forms.HiddenInput)
