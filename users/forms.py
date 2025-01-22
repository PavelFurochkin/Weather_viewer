from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator


class RegistrationForm(forms.ModelForm):
    username = forms.CharField(
        label='Логин',
        widget=forms.TextInput(attrs={"class": "form-control"}),
        required=True,
        validators=[
            MinLengthValidator(4, message="Логин должен быть не короче 4 символов"),
            MaxLengthValidator(25, message="Логин должен быть не длинее 25 символов"),
            UnicodeUsernameValidator(message='Логин может содержать только буквы, цифры и символ подчёркивания')
        ]
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        required=True,
        validators=[
            MinLengthValidator(8, message="Пароль должен быть не короче 8 символов"),
            MaxLengthValidator(20, message="Пароль должен быть не длинее 20 символов"),
        ]
    )

    password_check = forms.CharField(
        label='Подтверждение пароля',
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        required=True,
    )

    class Meta:
        model = get_user_model()
        fields = ['username', 'password', 'password_check']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])

        if commit:
            user.save()
        return user

    def clean_username(self):
        """ Проверяет уникальность логина."""

        username = self.cleaned_data['username'].strip()

        if not username:
            raise forms.ValidationError("Поле логин не должен быть пустым")

        if get_user_model().objects.filter(username=username).exists():
            raise forms.ValidationError("Пользователь с таким логином уже существует")

        return username

    def clean_password(self):
        """ Проверяет корректность ввода пароля"""

        password = self.cleaned_data.get('password', '')

        if not password:
            raise forms.ValidationError("Поле пароля не может быть пустым")

        return password

    def clean_password_check(self):
        """ Проверяет совместимость пароля."""

        password = self.cleaned_data.get('password')
        password_check = self.cleaned_data.get('password_check')

        if password != password_check:
            raise forms.ValidationError("Пароли не совпадают")

        return password_check


class AuthorizationForm(forms.Form):
    username = forms.CharField(
        label='Логин',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True,

    )

    password = forms.CharField(
        label='Введите пароль',
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Введите пароль', 'class': 'form-control'}),
        required=True
    )

    def __init__(self, *args, **kwargs):
        self.user_cache = None
        super().__init__(*args, **kwargs)

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username and password:
            self.user_cache = authenticate(username=username, password=password)
            if self.user_cache is None:
                raise ValidationError('Неверный логин или пароль')

    def get_user(self):
        return self.user_cache
