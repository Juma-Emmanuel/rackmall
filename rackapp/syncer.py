import firebase_admin
from firebase_admin import db
from .models import F_Cart, F_CartProduct
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
# Function to post data to Firebase


@receiver(post_save, sender=F_Cart)
def update_or_create_cart_product(sender, instance, created, **kwargs):
    # This function will be called after saving an F_CartProduct object
    # Use the 'created' flag to determine if it's a new creation or an update
    if created:
        # This is a new creation, so update Firebase accordingly
        # You can use the instance to get the data you want to send to Firebase
        data_to_update = {
            'customer_id': instance.customer.id if instance.customer else None,
            'total': instance.total
        }
        ref = db.reference('carts')  #
        ref.child(str(instance.id)).set(data_to_update)
    else:
        # This is an update, you can handle it here if needed
        # This is an update, so update Firebase accordingly
        # You can use the instance to get the data you want to send to Firebase
        data_to_update = {
          'customer_id': instance.customer.id if instance.customer else None,
            'total': instance.total
        }
        ref = db.reference('carts')  
        ref.child(str(instance.id)).update(data_to_update)
@receiver(post_save, sender=F_CartProduct)
def update_or_create_cart_product(sender, instance, created, **kwargs):
    # This function will be called after saving an F_CartProduct object
    # Use the 'created' flag to determine if it's a new creation or an update
    if created:
        # This is a new creation, so update Firebase accordingly
        # You can use the instance to get the data you want to send to Firebase
        data_to_update = {
            'product_id': instance.product.id,
            'rate': instance.rate,
            'quantity': instance.quantity,
            'subtotal': instance.subtotal
        }
        ref = db.reference('cart_products')  # Reference to the 'cart_products' node in Firebase
        ref.child(str(instance.id)).set(data_to_update)
    else:
        # This is an update, you can handle it here if needed
        # This is an update, so update Firebase accordingly
        # You can use the instance to get the data you want to send to Firebase
        data_to_update = {
            'product_id': instance.product.id,
            'rate': instance.rate,
            'quantity': instance.quantity,
            'subtotal': instance.subtotal
        }
        ref = db.reference('cart_products')  # Reference to the 'cart_products' node in Firebase
        ref.child(str(instance.id)).update(data_to_update)
@receiver(post_delete, sender=F_CartProduct)
def delete_cart_product(sender, instance, **kwargs):
    # This function will be called whenever an F_CartProduct object is deleted
    # You can use the instance to get the ID of the deleted object
    cart_product_id = instance.id

    # Now, you can update Firebase to reflect the deletion
    ref = db.reference('cart_products')  # Reference to the 'cart_products' node in Firebase
    ref.child(str(cart_product_id)).delete()


# Call the function to post data to Firebase
#post_data_to_firebase()

