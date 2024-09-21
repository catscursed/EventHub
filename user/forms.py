from django import forms
from django.core.exceptions import ValidationError
from .models import MyUser


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput)

    class Meta:
        model = MyUser
        fields = ('phone_number', 'first_name', 'email')

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if MyUser.objects.filter(phone_number=phone_number).exists():
            raise ValidationError('Этот номер телефона уже используется.')
        return phone_number

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if MyUser.objects.filter(email=email).exists():
            raise ValidationError('Этот адрес электронной почты уже используется.')
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Пароли не совпадают")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
