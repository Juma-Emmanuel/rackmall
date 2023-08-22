from typing import Any, Dict
import firebase_admin
from firebase_admin import db
from firebase_admin import storage
import datetime
from django.shortcuts import render, redirect
from .firebase_utils import push_data, get_data, upload_image
from .models import *


from django.views.generic import FormView
from django.views.generic import TemplateView
# Create your views here.

def post_product(request):    
    if request.method == 'POST':
        category = request.POST['category']
        title  = request.POST['title']
        description  = request.POST['description']
        marked_price  = request.POST['marked_price']
        selling_price  = request.POST['selling_price']
        return_policy  = request.POST['return_policy']
        warranty  = request.POST['warranty']
        url  = request.POST['url']

  # Post the data to Firebase
        
        data_to_post = {
            "title": title,
            "description": description,
            "marked_price": marked_price,
            "selling_price": selling_price,
            "warranty": warranty,
            "return_policy": return_policy,
            "url": url,
        }
        
        if category == 'lawn_tennis':
            response=push_data(data_to_post, "product/lawn_tennis")
        elif category == 'badminton':
            response=push_data(data_to_post, "product/badminton")
        elif category == 'table_tennis':
            response=push_data(data_to_post, "product/table_tennis")
        else:            
            response=push_data(data_to_post, "product/other")


    return render(request, 'post_product.html')
def post_data_view(request):
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



    return render(request, "post_data.html")

        
def data_list_view(request):
    data = get_data()
    return render(request, "data_list.html", {"data": data, })

class HomeView(TemplateView):
    template_name = "home.html"
 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['myname'] = "Juma Emmanuel"
        data1 = get_data("product/lawn_tennis")
        data2 = get_data("product/other")
        data3= get_data("data/")
        data4= get_data("product/")
        data5= get_data("product/")
        context['product_list1'] = data1
        context['product_list2'] = data2
        context['product_list3'] = data3
        return context

class AllProductsView(TemplateView):
    template_name = "allproducts.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['allcategories'] = Category.objects.all()
        
        return context

class ProductDetailView(TemplateView):
    template_name = "productdetail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['allcategories'] = Category.objects.all()
        slug = kwargs['slug']
        print(slug, "9999999")
        return context

class AboutView(TemplateView):
    template_name = "about.html"