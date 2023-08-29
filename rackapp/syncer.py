import firebase_admin
from firebase_admin import db
from .models import F_Cart, F_CartProduct
from .firebase_utils import *
from django.db.models.signals import post_save
from django.dispatch import receiver
# Function to post data to Firebase
ref = db.reference('')
def post_cart_to_firebase(cart):
    # Initialize Firebase Admin SDK (replace with your Firebase configuration)
      # Replace with your Firebase URL
    
    # Get data from Django admin database
    #carts = F_Cart.objects.all()

    #for cart in carts:
        # Create a new cart node in Firebase
    cart_ref = ref.child('carts').push({
            'customer_id': cart.customer.id if cart.customer else None,
            'total': cart.total
        })

    cart_id = cart_ref.key

        # Get cart products for this cart
    cart_products = F_CartProduct.objects.filter(cart=cart)

    for cart_product in cart_products:
            # Create a new cart product node in Firebase
            ref.child('cart_products').child(cart_id).push({
                'product_id': cart_product.product.id,
                'rate': cart_product.rate,
                'quantity': cart_product.quantity,
                'subtotal': cart_product.subtotal
            })
# Create a receiver function to listen for new cart data being saved in Django admin database
@receiver(post_save, sender=F_Cart)
def cart_post_save(sender, instance, **kwargs):
    post_cart_to_firebase(instance)

# Create a receiver function to listen for new cart product data being saved in Django admin database
@receiver(post_save, sender=F_CartProduct)
def cart_product_post_save(sender, instance, **kwargs):
    if instance.cart and instance.cart.id:
        post_cart_to_firebase(instance.cart)
# Call the function to post data to Firebase
#post_data_to_firebase()
