from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Product, Category
from django.contrib import messages


class HomeView(View):
    def get(self, request, *args, **kwargs):
        products = Product.objects.all()
        return render(request, "home/index.html", {"products": products})


class ProductDetailView(View):
    def get(self, request, *args, **kwargs):
        product = get_object_or_404(Product, slug=kwargs["slug"])
        return render(request, "home/detail.html", {"product": product})
