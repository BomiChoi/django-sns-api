from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from .models import User


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email',)

    def clean_password2(self):
        """ 비밀번호가 일치하는지 검사"""
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError("비밀번호가 일치하지 않습니다.")
        return password2

    def save(self, commit=True):
        """ 유저 생성 후 비밀번호 설정 """
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = (
            'email',
            'password',
            'name',
            'gender',
            'age',
            'phone',
            'is_staff',
            'is_superuser',
            'is_active',
        )


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    fieldsets = (
        (None, {
            'fields': (
                'email',
                'password',
            )
        }),
        ('Personal Info', {
            'fields': (
                'name',
                'gender',
                'age',
                'phone',
            )
        }),
        ('Permissions', {
            'fields': (
                'is_staff',
                'is_superuser',
            )
        })
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'password1',
                'password2',
            )
        }),
    )

    list_display = (
        'id',
        'email',
        'name',
        'gender',
        'age',
        'phone',
        'is_staff',
        'is_superuser',
        'is_active',
        'created_at',
        'updated_at',
    )

    ordering = ('email',)
