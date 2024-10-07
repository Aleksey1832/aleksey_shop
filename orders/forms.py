from django import forms
from orders.models import Order


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'first_name',
            'middle_name',
            'last_name',
            'gender',
            'date_birth',
            'phone_number',
            'email',
            'city',
            'street',
            'house_number',
            'litter_number',
            'apartments_number',
            'floor',
            'postal_code'
        ]
