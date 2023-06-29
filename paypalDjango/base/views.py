from django.shortcuts import render
from django.http import HttpResponse
import random

# Create your views here.

def simpleCheckout(request):
    return render(request, 'checkout.html')

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import base64

CLIENT_ID = "Ad6JDTCulsATrkE2ahNH7ZKHy9ZTnTuRlopsnrDbxKWPoEK4wz4yfiv_ZPweNtHYrYqEse3r4x23HrUx"
APP_SECRET = "EMQQbFuCHWWNYRg_J6o03a-xhPfTtFsN1AQwGrlc1ZaPbWItTdhJ47itjlKOncseElg1-qnenK2ZH7D3"
baseURL = {
    "sandbox": "https://api-m.sandbox.paypal.com",
    "production": "https://https://developer.paypal.com/"
}

@csrf_exempt
def create_paypal_order(request):
    if request.method == "POST":
        order = create_order()
        return JsonResponse(order)
    return JsonResponse({"message": "Invalid request method"})

@csrf_exempt
def capture_paypal_order(request):
    if request.method == "POST":
        order_id = request.POST.get("orderID")
        capture_data = capture_payment(order_id)
        # TODO: store payment information such as the transaction ID
        return JsonResponse(capture_data)
    return JsonResponse({"message": "Invalid request method"})

# PayPal API helpers

def create_order():
    access_token = generate_access_token()
    url = f"{baseURL['sandbox']}/v2/checkout/orders"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    payload = {
        "intent": "CAPTURE",
        "purchase_units": [
            {
                "amount": {
                    "currency_code": "USD",
                    "value": "10.00"
                }
            }
        ]
    }
    response = requests.post(url, headers=headers, json=payload)
    data = response.json()
    return data

def capture_payment(order_id):
    access_token = generate_access_token()
    url = f"{baseURL['sandbox']}/v2/checkout/orders/{order_id}/capture"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.post(url, headers=headers)
    data = response.json()
    print(data)
    return data

def generate_access_token():
    auth = base64.b64encode(f"{CLIENT_ID}:{APP_SECRET}".encode()).decode()
    url = f"{baseURL['sandbox']}/v1/oauth2/token"
    headers = {
        "Authorization": f"Basic {auth}"
    }
    payload = {
        "grant_type": "client_credentials"
    }
    response = requests.post(url, headers=headers, data=payload)
    data = response.json()
    return data["access_token"]

