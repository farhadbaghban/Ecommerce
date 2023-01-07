from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import User


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="password", widget=forms.PasswordInput())
    password2 = forms.CharField(label="confirm password", widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ("email", "phone_number", "full_name")

    def clean_password2(self):
        password1 = self.cleaned_data["password1"]
        password2 = self.cleaned_data["password2"]
        if password1 and password2 and password1 != password2:
            raise ValidationError("password dont match")
        return password2

    def save(self, commit: True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password2"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        help_text="you can changepassword by using <a href = ' ../password/'>this link</a>."
    )

    class Meta:
        model = User
        fields = ("email", "phone_number", "full_name", "password", "last_login")
