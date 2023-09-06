from django import forms
from .models import *
from django.contrib.auth.models import User
from django.views.generic.edit import FormView
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

class  CustRegistrationForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())
    email = forms.CharField(widget=forms.EmailInput())
    class Meta:
        model = Customer
        # "username","password","email", 
        fields = ["username", "password","email","full_name", "address"]

    def clean_username(self):
            uname = self.cleaned_data.get("username")
            if User.objects.filter(username=uname).exists():
                raise forms.ValidationError("this username already exists")
            return uname

class  CustLoginForm(forms.Form):
        username = forms.CharField(widget=forms.TextInput())
        password = forms.CharField(widget=forms.PasswordInput())

class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["ordered_by","shipping_address","mobile","email"]


     