from typing import Any, Dict
import firebase_admin
from firebase_admin import db
from firebase_admin import storage
import datetime
from django.shortcuts import render, redirect
from .firebase_utils import push_data, get_data, upload_image
from .models import *
from .fetch import *
from .syncer import *



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
            "category": category,
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
        post_cart = {
            "customer":"",
            "Total":"",
        }
        response=push_data(post_cart, "cart")
      
        

    return render(request, 'post_product.html')


    
def data_list_view(request):
    data = get_data()
    return render(request, "data_list.html", {"data": data, })

class HomeView(TemplateView):
    template_name = "home.html"
 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['myname'] = "Juma Emmanuel"
        context['product'] = Pro_duct.objects.all()
        context['product_list'] = get_data("product/")
        return context

class AllProductsView(TemplateView):
    template_name = "allproducts.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['allcategories'] = Category.objects.all()
        data= get_data("product/")
        context['product_list'] = data
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
class AddToCartView(TemplateView):
    template_name = 'addtocart.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        product_id = self.kwargs['pro_id']
         
        product_obj = Pro_duct.objects.get(id=product_id)
        
        cart_id = self.request.session.get("cart_id", None)
        if cart_id:
            
            cart_obj = F_Cart.objects.get(id=cart_id)
            this_product_in_cart = cart_obj.f_cartproduct_set.filter(
                product=product_obj)
            ''' cart_data = {
            'customer': cart_obj.customer, 
            'total': cart_obj.total,       
             # Add other fields as needed
             }'''
          
            # item already exists in cart
            if this_product_in_cart.exists():
                cartproduct= this_product_in_cart.last()
                

                cartproduct.quantity += 1
                cartproduct.subtotal += product_obj.selling_price
                cartproduct.save()
                
                cart_obj.total += product_obj.selling_price
                cart_obj.save()
                #update_data_to_firebase()
                '''cartproduct_data = {
                    
                   'cp_detail':{
                    'title': cartproduct.product.title,
                    'rate': cartproduct.rate,
                    'quantity': cartproduct.quantity,
                    'subtotal': cartproduct.subtotal

                }
                    }
                cartproduct_info.push(cartproduct_data)
                cart_info.set(cart_data)'''
                # new item is already in cart
                #update_data_in_firebase(cart_id)
                #post_cart_to_firebase(cart_obj)
                for p in this_product_in_cart:
                    print(p)
            else:
                cartproduct = F_CartProduct.objects.create(
                    cart=cart_obj, product=product_obj, rate=product_obj.selling_price, quantity=1, subtotal=product_obj.selling_price)
                
                cart_obj.total += product_obj.selling_price
                cart_obj.save()
               
                
        # create if cart doesn't exists                                                 
        else:
            cart_obj = F_Cart.objects.create(total=0)
            self.request.session['cart_id'] = cart_obj.id
            cartproduct = F_CartProduct.objects.create(
                    cart=cart_obj, product=product_obj, rate=product_obj.selling_price, quantity=1, subtotal=product_obj.selling_price)
            
            cart_obj.total += product_obj.selling_price
            cart_obj.save()
            
            
        
        
    
        return context

class MyCartView(TemplateView):
    template_name = "mycart.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_id = self.request.session.get("cart_id", None)
        if cart_id:
            cart = F_Cart.objects.get(id=cart_id)
        else:
            cart=None 
        context['cart'] = cart 
        return context
class ManageCartView(TemplateView):
        def get(self, request, *args, **kwargs):
            
            cp_id = self.kwargs["cp_id"]
            action = request.GET.get("action")
            cp_obj =F_CartProduct.objects.get(id=cp_id)
            cart_obj =cp_obj.cart
            
            
            if action == "inc":
                cp_obj.quantity += 1
                cp_obj.subtotal += cp_obj.rate
                cp_obj.save()
                cart_obj.total += cp_obj.rate
                cart_obj.save()
                #cart_info.set(cart_data)
                #cartproduct_info.update(cartproduct_data)
                cart_data={
               'total': cart_obj.total,
                }
                '''cartproduct_data = {
                    
               'product_id': cp_obj.product.id,
                 
                'rate': cp_obj.rate,
                    'quantity': cp_obj.quantity,
                'subtotal': cp_obj.subtotal
                 # Add other fields as needed
                 
                   }
                cartproduct_info.set({cp_id: cartproduct_data})'''
               
                #cart_info.set(cart_data)
                
                #update_cproduct_in_firebase()
                
            elif action == "dcr":
                 cp_obj.quantity -= 1
                 cp_obj.subtotal -= cp_obj.rate
                 cp_obj.save()
                 cart_obj.total -= cp_obj.rate
                 cart_obj.save()
                # cart_info.set(cart_data)
                 #cartproduct_info.set(cartproduct_data) 
                 cart_data={
                  'total': cart_obj.total,
                 }
                 '''cartproduct_data = {
             
                   'cp_detail':{
             
                 'title':cp_obj.product.title,
                'rate': cp_obj.rate,
                    'quantity': cp_obj.quantity,
                'subtotal': cp_obj.subtotal
                 # Add other fields as needed
                 }
                   }
                 cartproduct_info.update({cp_id: cartproduct_data})'''
                 cart_info.set(cart_data)
                # update_cproduct_in_firebase()
                 
                 
                     
                 
            elif action == "rmv":
                cart_obj.total -= cp_obj.subtotal
                cart_obj.save()
                cp_obj.delete() 
                
               # cart_info.set(cart_data)
                
                #cartproduct_info.delete(cartproduct_data)
                cart_data={
               'total': cart_obj.total,
                }
                cart_info.set(cart_data)
                #update_cproduct_in_firebase()
                
                                         
            else:
                pass
          
            
            
            
            
            
            
                  
            return redirect("rackapp:mycart")