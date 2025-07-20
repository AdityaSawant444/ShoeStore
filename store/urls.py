from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
    path('men/', views.men_shoes, name='men_shoes'),
    path('women/', views.women_shoes, name='women_shoes'),
    path('cart/', views.cart, name='cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('remove-from-cart/<int:product_id>/<str:size>/', views.remove_from_cart, name='remove_from_cart_with_size'),
    path('checkout/', views.checkout, name='checkout'),
    path('process-order/', views.process_order, name='process_order'),
    path('order-success/<str:order_number>/', views.order_success, name='order_success'),
    path('order/<str:order_number>/', views.order_detail, name='order_detail'),
    path('search/', views.search_products, name='search'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('profile/settings/', views.profile_settings, name='profile_settings'),
    path('size-guide/', views.size_guide, name='size_guide'),
    path('shipping-info/', views.shipping_info, name='shipping_info'),
    path('contact-support/', views.contact_support, name='contact_support'),
    path('track-order/', views.track_order, name='track_order'),
    path('test-form/', views.test_form, name='test_form'),
    path('test-cart/', views.test_cart, name='test_cart'),
] 