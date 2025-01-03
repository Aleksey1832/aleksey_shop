from django import forms

CHOICES = [(i, str(i)) for i in range(1, 11)]


class CartAddProductForm(forms.Form):
    """ Класс формы для добавления количества товара в корзину """
    quantity = forms.TypedChoiceField(
        choices=CHOICES,
        coerce=int,
        label='Количество'
    )

    override = forms.BooleanField(
        required=False,
        widget=forms.HiddenInput
    )
