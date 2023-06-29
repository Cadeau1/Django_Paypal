from django.contrib import admin
from django.urls import path,include
from .views import *
# from myapp.views import create_paypal_order, capture_paypal_order

app_name="base"


urlpatterns = [
    path('checkout/', simpleCheckout), 
    path("create-paypal-order", create_paypal_order),
    path("capture-paypal-order", capture_paypal_order),  
]