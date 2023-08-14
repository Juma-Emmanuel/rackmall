from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    #path('', views.data_list_view, name="data_list_view"),
    #path('', views.index, name="index"),
    path('', views.post_data_view, name="post_data_view"),
    path('data-list/', views.data_list_view, name="data_list_view"),
]