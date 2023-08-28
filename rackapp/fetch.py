from .firebase_utils import *
import firebase_admin
from firebase_admin import credentials, db
from .models import *
from django.conf import settings
# Initialize Firebase Admin SDK (replace with your own Firebase configuration)
ref = db.reference('')
product_data = ref.child('product').get()
#cart_info = db.reference('cart')
cart_info=ref.child('carts')
cartproduct_info=ref.child('cart_products')



# Fetch data from Firebase




for product_id, pro_category in product_data.items():
    for p, pro_item in pro_category.items():
        title = pro_item.get('title', '')
        url = pro_item.get('url', '')
        marked_price = pro_item.get('marked_price', '')
        selling_price = pro_item.get('selling_price', '')
        description = pro_item.get('description', '')
        return_policy = pro_item.get('return_policy', '')
        warranty = pro_item.get('warranty', '')
       
        print(title)

        # Create Django model instances
        product = Pro_duct.objects.create(title=title, url=url, marked_price=marked_price, warranty=warranty, selling_price=selling_price, description=description, return_policy=return_policy)


