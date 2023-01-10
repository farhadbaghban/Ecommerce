from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserRegisterForm, UserVerifyForm, UserLoginForm
from .models import User, OtpCode
from utils import send_otp_code
from django.utils import timezone
import random


class UserRegisterView(View):
    form_class = UserRegisterForm
    template_class = "accounts/register.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home:home_view")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class
        return render(request, self.template_class, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            random_code = random.randint(1000, 9999)
            # send_otp_code(cd["phone_number"], random_code)
            OtpCode.objects.create(phone_number=cd["phone_number"], code=random_code)
            request.session["user_registeration_info"] = {
                "phone_number": cd["phone_number"],
                "full_name": cd["full_name"],
                "email": cd["email"],
                "password": cd["password2"],
            }
            messages.success(request, "We sent a code to your phone number", "success")
            return redirect("accounts:verify_code")
        return redirect(self.template_class, {"form": form})


class UserRegisterVerifyView(View):
    form_class = UserVerifyForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home:home_view")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class
        return render(request, "accounts/verify.html", {"form": form})

    def post(self, requset, *args, **kwargs):
        form = self.form_class(requset.POST)
        user_info = requset.session["user_registeration_info"]
        if form.is_valid():
            cd = form.cleaned_data
            code_instance = OtpCode.objects.get(phone_number=user_info["phone_number"])
            timeout = timezone.now().replace(microsecond=0)
            seconds_ago = (
                timeout - code_instance.created.replace(microsecond=0)
            ).seconds
            if seconds_ago < 179:
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
            else:
                code_instance.delete()
                messages.error(requset, "This code has expired", "danger")
                return redirect("accounts:user_register")
        return redirect("home:home_view")


class UserLoginView(View):
    form_class = UserLoginForm
    tem_class = "accounts/login.html"

    def setup(self, request, *args, **kwargs):
        self.next = request.GET.get("next")
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home:home_view")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class
        return render(request, self.tem_class, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request, phone_number=cd["phone_number"], password=cd["password"]
            )
            if user is not None:
                login(request, user)
                messages.success(request, "You are login", "success")
                if self.next:
                    return redirect(self.next)
                return redirect("home:home_view")
            messages.error(request, "username or password is Wrong", "warning")
        return render(request, self.tem_class, {"form": form})


class UserLogoutView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, "You Log Out", "success")
        return redirect("home:home_view")
