from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from .forms import UserRegisterForm, UserVerifyForm
from .models import User, OtpCode
from utils import send_otp_code
import random


class UserRegisterView(View):
    form_class = UserRegisterForm

    def get(self, request, *args, **kwargs):
        form = self.form_class
        return render(request, "accounts/register.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            random_code = random.randint(1000, 9999)
            send_otp_code(cd["phone_number"], random_code)
            OtpCode.objects.create(phone_number=cd["phone_number"], code=random_code)
            request.session["user_registeration_info"] = {
                "phone_number": cd["phone_number"],
                "full_name": cd["full_name"],
                "email": cd["email"],
                "password": cd["password2"],
            }
            messages.success(request, "We sent a code to your phone number", "success")
            return redirect("accounts:verify_code")
        return redirect("home:home_view")


class UserRegisterVerifyView(View):
    form_class = UserVerifyForm

    def get(self, request, *args, **kwargs):
        form = self.form_class
        return render(request, "accounts/verify.html", {"form": form})

    def post(self, requset, *args, **kwargs):
        form = self.form_class(requset.POST)
        user_info = requset.session["user_registeration_info"]
        if form.is_valid():
            cd = form.cleaned_data
            code_instance = OtpCode.objects.get(phone_number=user_info["phone_number"])
            if int(cd["verify_code"]) == code_instance.code:
                User.objects.create_user(
                    user_info["email"],
                    user_info["phone_number"],
                    user_info["full_name"],
                    user_info["password"],
                )
                code_instance.delete()
                messages.success(requset, "You are registered", "success")
                return redirect("home:home_view")
            else:
                messages.error(requset, "This code is Wrong", "danger")
                return redirect("accounts:verify_code")
        return redirect("home:home_view")
