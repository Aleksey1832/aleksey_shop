from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from accounts.models import Profile, Address


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Username',
        'autofocus': 'autofocus'
    }),
        label='Имя пользователя'
    )
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password',
        'autofocus': 'autofocus'
    }),
        label='Пароль'
    )


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'autofocus': 'autofocus',
        'class': 'form-control'
    }),
        max_length=30,
        min_length=3,
        required=True,
        label='Логин'
    )
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'autofocus': 'autofocus',
        'class': 'form-control'
    }),
        max_length=30,
        required=True,
        label='Имя'
    )
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'autofocus': 'autofocus',
        'class': 'form-control'
    }),
        max_length=150,
        required=True,
        label='Фамилия'
    )
    email = forms.EmailField(widget=forms.TextInput(attrs={
        'autofocus': 'autofocus',
        'class': 'form-control'
    }),
        max_length=254,
        required=True,
        label='Email'
    )
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'autofocus': 'autofocus',
        'class': 'form-control'
    }),
        label='Пароль'
    )
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'autofocus': 'autofocus',
        'class': 'form-control'
    }),
        label='Подтверждение пароля'
    )

    birth_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date', 'autofocus': 'autofocus'}),
                                 required=True,
                                 label='Дата рождения')
    # gender = forms.CharField(max_length=7, required=True, label='Пол')
    # tel = forms.CharField(max_length=11, required=True, label='Телефон')
    # postal_code = forms.CharField(max_length=5, required=True, label='Почтовый индекс')
    # city = forms.CharField(max_length=50, required=True, label='Город')
    # street = forms.CharField(max_length=50, required=True, label='Улица')
    # address = forms.CharField(max_length=100, required=True, label='Дом/корпус, кв. или офис')

    def save(self, commit=True):  # эти поля создаются при первичной регистрации на сайте
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            profile = Profile.objects.get(user=user)
            profile.birth_date = self.cleaned_data['birth_date']
            profile.email = self.cleaned_data['email']
            profile.save()
        return user


class ProfileEditForm(forms.ModelForm):
    gender = forms.ChoiceField(choices=[
        ('', 'Выберите пол'),
        ('Женский', 'Женский'),
        ('Мужской', 'Мужской'),
    ], widget=forms.Select(attrs={'class': 'form-control'}), label='Выбрать пол')

    class Meta:
        model = Profile
        fields = [
            'gender',
            'phone_number',

            # 'birth_date'
            # 'country',
            # 'region',
            # 'city',
            # 'street',
            # 'house_number',
            # 'litter_number',
            # 'apartments_number',
            # 'postal_code'
        ]
        labels = [
            'Пол',
            'Телефон',
            # 'Дата рождения'
            # 'Страна',
            # 'Регион',
            # 'Город',
            # 'Улица',
            # 'Номер дома',
            # 'Корпус/литера/строение',
            # 'Квартира/помещение',
            # 'Почтовый код'
        ]

    def __init__(self, *args, **kwargs):
        super(ProfileEditForm, self).__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({'class': 'form-control', 'autofocus': 'autofocus'})


class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'autofocus': 'autofocus',
        'class': 'form-control'
    }),
        label='Старый пароль'
    )
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'autofocus': 'autofocus',
        'class': 'form-control'
    }),
        label='Новый пароль'
    )
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'autofocus': 'autofocus',
        'class': 'form-control'
    }),
        label='Новый пароль (подтверждение)'
    )


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = [
            'country',
            'region',
            'city',
            'street',
            'house_number',
            'litter_number',
            'apartments_number',
            'floor',
            'elevator',
            'intercom',
            'postal_code'
        ]

    def __init__(self, *args, **kwargs):
        super(AddressForm, self).__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({'class': 'form-control', 'autofocus': 'autofocus'})
