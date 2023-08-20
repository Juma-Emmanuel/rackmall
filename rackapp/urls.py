from django.contrib import admin
from django.urls import path
from . import views
from .views import *
app_name = "rackapp"
urlpatterns = [
    #path('', views.data_list_view, name="data_list_view"),
    #path('', views.index, name="index"),
    path('', views.post_data_view, name="post_data_view"),
    path('data-list/', views.data_list_view, name="data_list_view"),

 
    #path('', HomeView.as_view(), name="home"),
    path("about/", AboutView.as_view(), name="about"),
    path("allproducts/", AllProductsView.as_view(), name="allproducts"),
    path("product/<slug:slug>/", ProductDetailView.as_view(), name="productdetail"),

]