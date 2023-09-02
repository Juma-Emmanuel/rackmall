from django import forms
from .models import *

from django.views.generic.edit import FormView
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
        