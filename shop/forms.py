from django import forms


SORT_CHOICES = [
    ('default', 'По умолчанию'),
    ('name', 'По имени'),
    ('price_asc', 'Цена по возрастанию'),
    ('price_desc', 'Цена по убыванию')
]


class ShopFormSorted(forms.Form):
    form_sorted = forms.ChoiceField(
        choices=SORT_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'autofocus': 'autofocus'
        }),
        label=''
    )
