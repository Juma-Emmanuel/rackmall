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

            if image:
                image_url = upload_image(image.read(), image.name)
                # Save the image URL in the Realtime Database under the specific data key
                db.reference(f"data/{data_key}").update({"image_url": image_url})

        return redirect("data_list_view")

    return render(request, "post_data.html")

        
def data_list_view(request):
    data = get_data()
    return render(request, "data_list.html", {"data": data, })
class HomeView(TemplateView):
    template_name = "home.html"
 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['myname'] = "Juma Emmanuel"
        context['product_list'] = Product.objects.all().order_by("-id")
        
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