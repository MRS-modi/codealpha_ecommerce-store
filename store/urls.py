from django.urls import path
from . import views

urlpatterns = [
    path('', views.store, name="store"),
    path('product/<int:pk>/', views.product_detail, name="product_detail"),
    path('add-to-cart/<int:pk>/', views.add_to_cart, name="add_to_cart"),
    path('cart/', views.cart, name="cart"),
    path('update-quantity/<int:item_id>/<str:action>/', views.update_item_quantity, name="update_quantity"),
    path('checkout/', views.checkout, name="checkout"),
    path('process-order/', views.process_order, name="process_order"),
    path('order-success/', views.order_success, name="order_success"),
    path('register/', views.register_user, name="register"),
    path('login/', views.login_user, name="login"),
    path('logout/', views.logout_user, name="logout"),
]