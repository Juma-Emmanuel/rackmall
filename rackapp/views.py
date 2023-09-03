from typing import Any, Dict
import firebase_admin

from firebase_admin import firestore
import datetime
from django.shortcuts import render, redirect
import requests

from .models import *

from .forms import *
import json
import os
from django.views.generic import FormView
from django.views.generic import TemplateView

# db=firestore.Client()
# # Create your views here.
'''def post_product(request):    
    if request.method == 'POST':
        if 'post_data' in request.POST:
            category = request.POST['category']
            title  = request.POST['title']
            description  = request.POST['description']
            marked_price  = request.POST['marked_price']
            selling_price  = request.POST['selling_price']
            return_policy  = request.POST['return_policy']
            warranty  = request.POST['warranty']
            url  = request.POST['url']
            data_to_post = {
            "title": title,
            "category": category,
            "description": description,
            "marked_price": marked_price,
            "selling_price": selling_price,
            "warranty": warranty,
            "return_policy": return_policy,
            "url": url,
            }
            push_data(data_to_post, "products")
        elif 'add_category' in request.POST:
            new_category = request.POST['new_category']

            category_to_post = {
            "title":new_category,
              }
            response = push_data(category_to_post, "categories")

        
        if category == 'lawn_tennis':
            response=push_data(data_to_post, "product/lawn_tennis")
        elif category == 'badminton':
            response=push_data(data_to_post, "product/badminton")
        elif category == 'table_tennis':
            response=push_data(data_to_post, "product/table_tennis")
        else:            
            response=push_data(data_to_post, "product/other")
        
        
        
      
        

    return render(request, 'post_product.html')'''


# class FirebaseDataView(TemplateView):
#     template_name = 'trialview.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)

#         # Retrieve data from Firebase
#         data = get_data("student/")

#         context['datalist'] = data  # Pass the data to the template
#         return context
class AddToCartView(TemplateView):
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

class MyCartView(TemplateView):
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

class ManageCartView(TemplateView):
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

class EmptyCartView(TemplateView):
    def get(self, request, *args, **kwargs):
         cart_id = request.session.get("cart_id", None)
         if cart_id:
             cart = Cart.objects.get(id=cart_id)
             cart.cartproduct_set.all().delete()
             cart.total = 0
             cart.save()
         return redirect("rackapp:mycart")

'''def post_data_to_firebase(request): 
    if request.method == 'POST':
        campus = request.POST['campus']
        course = request.POST['course']
        cunit1 = request.POST['cunit1']
        cunit2 = request.POST['cunit2']

        # Create a Django model instance and save it to the database
        
        

        # Post the data to Firebase
        data_to_post = {
            "campus": campus,
            "course": course,
            "units": {
                "cunits": {
                    "cunit1": cunit1,
                    "cunit2": cunit2,
                }
        },
            # Add other fields as needed
        }
        response=push_data(data_to_post, "student/file")


    return render(request, 'trialpost.html')'''

'''def post_data_view(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        url = request.POST.get("url")
        image = request.FILES.get("image")

        data = {
            "title": title,
            "description": description,
            'url': url, 
        }

        # Call push_data to post the data and get the response
        response = push_data(data)

        if response.status_code == 200:
            # Parse the response JSON to get the generated key
            response_data = response.json()
            data_key = response_data.get("name")

            if image:
                image_url = upload_image(image.read(), image.name)
                # Save the image URL in the Realtime Database under the specific data key
                db.reference(f"data/{data_key}").update({"image_url": image_url})

        return redirect("data_list_view")

    return render(request, "post_data.html")'''

        
# def data_list_view(request):
#     data = get_data()
#     return render(request, "data_list.html", {"data": data, })
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