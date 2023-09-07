from django.contrib import admin
from django.urls import path
from . import views
from .views import *
app_name = "rackapp"
urlpatterns = [
    #path('', views.data_list_view, name="data_list_view"),
    #path('', views.index, name="index"),
    
#     path('data-list/', views.data_list_view, name="data_list_view"),
#     #path('post_product/', views.post_product, name="post_product"),
   
        path('create_category/', views.create_category, name="create_category"),
    path('create_product/', views.create_product, name="create_product"),

 
    path('', HomeView.as_view(), name="home"),
    path("about/", AboutView.as_view(), name="about"),
    path("allproducts/", AllProductsView.as_view(), name="allproducts"),
    path("product/<slug:slug>/", ProductDetailView.as_view(), name="productdetail"),
    path("addtocart/<int:pro_id>/", AddToCartView.as_view(), name="addtocart"),
    path("mycart/", MyCartView.as_view(), name="mycart"),
    path("managecart/<int:cp_id>", ManageCartView.as_view(), name="managecart"),
    path("emptycart/", EmptyCartView.as_view(), name="emptycart"),
    path("checkout/", CheckoutView.as_view(), name="checkout"),
    path("register/",CustRegistrationView.as_view(), name="register"),
    path("logout/",CustLogoutView.as_view(), name="logout"),
    path("login/",CustLoginView.as_view(), name="login"),
    path("profile/",CustProfileView.as_view(), name="profile"),
    path("profile/order<int:pk>/",CustOrderDetailView.as_view(), name="orderdetail"),
    path("admin-login/",AdminLoginView.as_view(), name="adminlogin"),
    path("admin-home/",AdminHomeView.as_view(), name="admin-home"),
    path("admin-order/<int:pk>/", AdminOrderDetailView.as_view(), name="adminorderdetail"),
    path("admin-all-orders/",AdminOrderListView.as_view(), name="adminorderlist"),
    path("Aregister/",AdminRegistrationView.as_view(), name="Aregister"),




]