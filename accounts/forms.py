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

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
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


class UserRegisterForm(forms.Form):
    phone_number = forms.CharField(max_length=11, label="phone number")
    email = forms.EmailField()
    full_name = forms.CharField(max_length=100, label="full name")
    password1 = forms.CharField(
        max_length=255, widget=forms.PasswordInput, label="password"
    )
    password2 = forms.CharField(
        max_length=255, widget=forms.PasswordInput, label="confirm password"
    )

    def clean_password2(self):
        password1 = self.cleaned_data["password1"]
        password2 = self.cleaned_data["password2"]
        if password1 and password2 and password1 != password2:
            raise ValidationError("password dont match")
        return password2

    def uniqe_email(self):
        email = self.cleaned_data["email"]
        user = User.objects.filter(email=email)
        if user:
            raise ValidationError("You cant use this Email Address")
        return email

    def uniqe_phone_number(self):
        phone_number = self.cleaned_data["phone_number"]
        user = User.objects.filter(phone_number=phone_number)
        if user:
            raise ValidationError("you cant use this phone Number")
        return phone_number


class UserVerifyForm(forms.Form):
    verify_code = forms.CharField(max_length=4, label="Verify Code")
