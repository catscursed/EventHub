from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from .models import MyUser


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput)

    class Meta:
        model = MyUser
        fields = ('phone_number', 'first_name', 'email')

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


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = MyUser
        fields = ('password', 'is_admin')


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('first_name', 'phone_number', 'created_date', 'status', 'is_admin')
    list_filter = ('is_admin', 'status', 'created_date')
    fieldsets = (
        (None, {
            'fields': (
                'password',
                'first_name',
                'last_name',
                'phone_number',
                'email',
                'cover',
                'wallet',
                'status'
            )
        }),
        ('Permissions', {'fields': ('is_admin',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'first_name',
                'phone_number',
                'password1',
                'password2'
            ),
        }),
    )
    search_fields = ('phone_number', 'first_name', 'email')
    ordering = ('phone_number',)
    filter_horizontal = ()


admin.site.register(MyUser, UserAdmin)
