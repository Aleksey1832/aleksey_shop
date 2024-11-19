from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Username',
        'autofocus': 'autofocus'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password',
        'autofocus': 'autofocus'
    }))


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'autofocus': 'autofocus'}),
                               max_length=30,
                               min_length=3,
                               required=True,
                               label='Логин')
    first_name = forms.CharField(widget=forms.TextInput(attrs={'autofocus': 'autofocus'}),
                                 max_length=30,
                                 required=True,
                                 label='Имя')
    last_name = forms.CharField(widget=forms.TextInput(attrs={'autofocus': 'autofocus'}),
                                max_length=150,
                                required=True,
                                label='Фамилия')
    email = forms.CharField(widget=forms.TextInput(attrs={'autofocus': 'autofocus'}),
                            max_length=254,
                            required=True,
                            label='Email')
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'autofocus': 'autofocus'}),
                                label='Пароль')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'autofocus': 'autofocus'}),
                                label='Подтверждение пароля')
