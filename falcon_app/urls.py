from django.urls import path
from .views import *

urlpatterns = [
    path('',index, name="index"),

    path('register_page/',register_page, name="register_page"),
    path('login_page/',login_page, name="login_page"),
    path('log_out/',log_out, name="log_out"),
    path('contact_page/',contact_page, name="contact_page"),
    path('profile_page/',profile_page, name="profile_page"),
    path('shop_page/',shop_page, name="shop_page"),
    path('product_details_page/<int:pk>/',product_details_page, name="product_details_page"),
    path('change_pass/',change_pass, name="change_pass"),

    path('cart_page/',cart_page, name="cart_page"),
    path('add_to_cart/<int:pk>/',add_to_cart, name="add_to_cart"),
    path('delete_cart_product/<int:pk>/',delete_cart_product, name="delete_cart_product"),

    path('add_to_wishlist/<int:pk>/',add_to_wishlist, name="add_to_wishlist"),
    path('delete_wishlist/<int:pk>/',delete_wishlist, name="delete_wishlist"),
    path('wishlist/',wishlist, name="wishlist"),

    path('checkout_page/',checkout_page, name="checkout_page"),

    # seller
    
    path('seller_index/',seller_index, name="seller_index"),

    path('seller_register/',seller_register, name="seller_register"),
    path('seller_login/',seller_login, name="seller_login"),
    path('seller_profile/',seller_profile, name="seller_profile"),
    path('seller_change_pass/',seller_change_pass, name="seller_change_pass"),
    path('seller_log_out/',seller_log_out, name="seller_log_out"),

    path('add_product/',add_product, name="add_product"),
    path('edit_product/<int:pk>/',edit_product, name="edit_product"),
    path('delete_product/<int:pk>/',delete_product, name="delete_product"),
    path('view_product/<int:pk>/',view_product, name="view_product"),

    # paytm section

    path('pay/', initiate_payment, name='pay'),
    path('callback/', callback, name='callback'),

]