from typing import Any, Dict
from django import http
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from .models import Customer
import datetime
from django.shortcuts import render, redirect
import requests
from django.contrib.auth import authenticate, login, logout
from .models import *
from django.urls import reverse_lazy
from .forms import *
import json
import os
from django.views.generic import FormView
from django.views.generic import View, TemplateView, CreateView, DetailView

# db=firestore.Client() 
# # Create your views here.
class RackMixin(object):
    def dispatch(self, request, *args, **kwargs):
        cart_id = request.session.get("cart_id")
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            if request.user.is_authenticated and request.user.customer:
                cart_obj.customer = request.user.customer
                cart_obj.save()
            return super().dispatch(request, *args, **kwargs)
class CustRegistrationView(CreateView):
    template_name = "custregistration.html"
    form_class = CustRegistrationForm
    success_url = reverse_lazy("rackapp:home")

    def form_valid(self, form):
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        email = form.cleaned_data.get("email")
        
        user = User.objects.create_user(username,email, password)
        form.instance.user = user
        login(self.request, user)
        return super().form_valid(form)
    def get_success_url(self):
        if "next" in self.request.GET:
            next_url = self.request.GET.get("next")
            return next_url
        else:
            return self.success_url

class CustLoginView(FormView):
    template_name = "custlogin.html"
    form_class = CustLoginForm    
    success_url = reverse_lazy("rackapp:home")

    def form_valid(self, form):
        uname = form.cleaned_data.get("username")
        pword = form.cleaned_data.get("password")
        usr = authenticate(username=uname, password=pword)
        if usr is not None and Customer.objects.filter(user=usr).exists():
            login(self.request, usr)
        else:
            return render(self.request, self.template_name, {"form": self.form_class, "error": "Invalid Credentials"})
        return super().form_valid(form)
    def get_success_url(self):
        if "next" in self.request.GET:
            next_url = self.request.GET.get("next")
            return next_url
        else:
            return self.success_url

class CustLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("rackapp:home")
    
class CustProfileView(TemplateView):
    template_name = "custprofile.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and Customer.objects.filter(user=request.user).exists():
            pass
        else:
            return redirect("/login/?next=/profile")

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs )
        customer = self.request.user.customer
        context['customer'] = customer 
        orders = Order.objects.filter(cart__customer=customer).order_by("-id")
        context["orders"] = orders
        return context

class CustOrderDetailView(DetailView):
    template_name = "orderdetail.html"
    model = Order
    context_object_name = "ord_obj"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and Customer.objects.filter(user=request.user).exists():
            order_id = self.kwargs["pk"]
            order = Order.objects.get(id=order_id)
            if request.user.customer != order.cart.customer:
                return redirect("rackapp:profile")
        else:
            return redirect("/login/?next=/profile/")

        return super().dispatch(request, *args, **kwargs)


class AddToCartView(RackMixin, TemplateView):
    template_name = 'addtocart.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        product_id = self.kwargs['pro_id']
         
        product_obj = Product.objects.get(id=product_id)
        
        cart_id = self.request.session.get("cart_id", None)
        # if cart exists
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            this_product_in_cart = cart_obj.cartproduct_set.filter(
                product=product_obj)
            # item already exists in cart
            if this_product_in_cart.exists():
                cartproduct= this_product_in_cart.last()
                cartproduct.quantity += 1
                cartproduct.subtotal += product_obj.selling_price
                cartproduct.save()
                cart_obj.total += product_obj.selling_price
                cart_obj.save()
                # new item is already in cart
            else:
                cartproduct = CartProduct.objects.create(
                    cart=cart_obj, product=product_obj, rate=product_obj.selling_price, quantity=1, subtotal=product_obj.selling_price)
                cart_obj.total += product_obj.selling_price
                cart_obj.save()
        # create if cart doesn't exists                                                 
        else:
            cart_obj = Cart.objects.create(total=0)
            self.request.session['cart_id'] = cart_obj.id
            
    
        return context

class MyCartView(RackMixin, TemplateView):
    template_name = "mycart.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_id = self.request.session.get("cart_id", None)
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
        else:
            cart=None 
        context['cart'] = cart 
        return context

class ManageCartView(RackMixin, TemplateView):
        def get(self, request, *args, **kwargs):
            
            cp_id = self.kwargs["cp_id"]
            action = request.GET.get("action")
            cp_obj =CartProduct.objects.get(id=cp_id)
            cart_obj =cp_obj.cart
            
            if action == "inc":
                cp_obj.quantity += 1
                cp_obj.subtotal += cp_obj.rate
                cp_obj.save()
                cart_obj.total += cp_obj.rate
                cart_obj.save() 
            elif action == "dcr":
                 cp_obj.quantity -= 1
                 cp_obj.subtotal -= cp_obj.rate
                 cp_obj.save()
                 cart_obj.total -= cp_obj.rate
                 cart_obj.save() 
                 if cp_obj.quantity == 0:
                     cp_obj.delete() 
            elif action == "rmv":
                cart_obj.total -= cp_obj.subtotal
                cart_obj.save()
                cp_obj.delete()                            
            else:
                pass
            return redirect("rackapp:mycart")

class EmptyCartView(RackMixin, TemplateView):
    def get(self, request, *args, **kwargs):
         cart_id = request.session.get("cart_id", None)
         if cart_id:
             cart = Cart.objects.get(id=cart_id)
             cart.cartproduct_set.all().delete()
             cart.total = 0
             cart.save()
         return redirect("rackapp:mycart")

class CheckoutView(RackMixin, CreateView):
    template_name = "checkout.html"
    form_class = CheckoutForm
    success_url = reverse_lazy("rackapp:home")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.customer:
            pass
        else:
            return redirect("/login/?next=/checkout/")

        return super().dispatch(request, *args, **kwargs)
 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_id = self.request.session.get("cart_id", None)
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
        else:
            cart_obj=None 
        context['cart'] = cart_obj
        return context 
    def form_valid(self, form):
        cart_id = self.request.session.get("cart_id")
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            form.instance.cart = cart_obj
            form.instance.subtotal = cart_obj.total
            form.instance.discount = 0
            form.instance.total = cart_obj.total
            form.instance.order_status = "Order Received"
            del self.request.session['cart_id']
        else:
            return redirect("rackapp:home")
        return super().form_valid(form)

class HomeView(TemplateView):
    template_name = "home.html"
 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['myname'] = "Juma Emmanuel"
        context['product_list'] = Product.objects.all().order_by("-id")
        context['product'] = Product.objects.all()
        return context

class AllProductsView(TemplateView):
    template_name = "allproducts.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['allcategories'] = Category.objects.all()
        context['pro_duct'] = Product.objects.all()
        return context

class ProductDetailView(TemplateView):
    template_name = "productdetail.html"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        url_slug = self.kwargs['slug']
        product= Product.objects.get(slug=url_slug)
        product.view_count += 1
        product.save()
        context['product'] = product
        return context


class AboutView(TemplateView):
    template_name = "about.html"

class AdminRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and Admin.objects.filter(user=request.user).exists():
            pass
        else:
            return redirect("/login/?next=/profile")

        return super().dispatch(request, *args, **kwargs) 

class AdminLoginView(FormView):
    template_name = "adminpages/adminlogin.html"
    form_class = CustLoginForm
    success_url = reverse_lazy("rackapp:admin-home")

    def form_valid(self, form):
        uname = form.cleaned_data.get("username")
        pword = form.cleaned_data.get("password")
        usr = authenticate(username=uname, password=pword)
        if usr is not None and Admin.objects.filter(user=usr).exists():
            login(self.request, usr)
        else:
            return render(self.request, self.template_name, {"form": self.form_class, "error": "Invalid Credentials"})
        return super().form_valid(form)


        

class AdminHomeView(FormView):
    template_name = "adminpages/adminhome.html"
    form_class = CustLoginForm
    success_url = reverse_lazy("rackapp:adminhome")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and Admin.objects.filter(user=request.user).exists():
            pass
        else:
            return redirect("/login/?next=/profile")

        return super().dispatch(request, *args, **kwargs) 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pendingorders"] = Order.objects.filter(
            order_status = "Order Received")

        return context

class AdminOrderDetailView(DetailView):
    template_name = "adminpages/adminorderdetail.html"
    model = Order
    context_object_name = "ord_obj"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and Admin.objects.filter(user=request.user).exists():
            pass
        else:
            return redirect("/login/?next=/profile")

        return super().dispatch(request, *args, **kwargs) 

def create_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            # Create an instance of the S_Product model
            form.save()
            return render(request, 'about.html')

    else:
        #print('nooooooooo')
        form =CategoryForm()   

    return render(request, 'category_form.html', {'form': form})

def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            # Create an instance of the Product model but don't save it to the database yet
            form.save()
            # Redirect to a success page or do something else
            return render(request, 'about.html')

    else:
         form = ProductForm()

    return render(request, 'product_form.html', {'form': form})