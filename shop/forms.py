from django import forms
from shop.models import Review
from django.conf import settings
from mixin.form_mixin import RecaptchaFormMixin


class ShopFormSorted(forms.Form):
    """ Сортировка товаров """
    form_sorted = forms.ChoiceField(
        choices=settings.SORT_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'autofocus': 'autofocus'
        }),
        label=''
    )


class ReviewAddForm(RecaptchaFormMixin, forms.ModelForm):
    """
        Определяет форму для добавления отзыва к товару, позволяет связать форму с моделью Review
    """
    rating = forms.IntegerField(widget=forms.HiddenInput(), initial=3)

    class Meta:
        """ Метакласс для определения настроек формы, связанных с моделью Review """
        model = Review
        fields = ['rating', 'text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 4}),
            'rating': forms.RadioSelect(choices=settings.RATING_CHOICES),
        }
        labels = {
            'text': 'Текст отзыва:',
            'rating': 'Рейтинг товара:'
        }
