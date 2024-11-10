from django import forms


SORT_CHOICES = [
    ('default', 'По умолчанию'),
    ('name', 'По имени'),
    ('price_asc', 'Цена по возрастанию'),
    ('price_desc', 'Цена по убыванию')
]


class ShopFormSorted(forms.Form):
    form_sorted = forms.TypedChoiceField(
        label='',
        choices=SORT_CHOICES,
        coerce=str
    )
    override = forms.BooleanField(
        required=False,
        widget=forms.HiddenInput
    )
