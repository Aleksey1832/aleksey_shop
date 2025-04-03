from django import forms
from shop.models import Review
from django.conf import settings


SORT_CHOICES = [
    ('default', 'По умолчанию'),
    ('name', 'По имени'),
    ('price_asc', 'Цена по возрастанию'),
    ('price_desc', 'Цена по убыванию')
]


class ShopFormSorted(forms.Form):
    """ Сортировка товаров """
    form_sorted = forms.ChoiceField(
        choices=SORT_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'autofocus': 'autofocus'
        }),
        label=''
    )


class ReviewAddForm(forms.ModelForm):
    """
        Определяет форму для добавления отзыва к товару.
        Наследуется от forms.ModelForm, что позволяет связать форму с моделью Review
    """
    class Meta:
        """ Метакласс для определения настроек формы, связанных с моделью Review """
        model = Review
        fields = ['rating', 'text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 4}),
            'rating': forms.RadioSelect(choices=settings.RATING_CHOICES),
        }
