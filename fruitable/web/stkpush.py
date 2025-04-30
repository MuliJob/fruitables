"""Sending STK Push to M-Pesa API"""
import json
from datetime import datetime
import base64
import requests

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings


def initiate_stk_push(phone, amount):
    """Send STK Push to Safaricom API"""
    try:
        consumer_key = settings.MPESA_CONSUMER_KEY
        consumer_secret = settings.MPESA_CONSUMER_SECRET
        auth_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
        r = requests.get(auth_url, auth=(consumer_key, consumer_secret), timeout=10)
        access_token = r.json().get('access_token')

        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        shortcode = settings.MPESA_SHORTCODE
        passkey = settings.MPESA_PASSKEY
        data_to_encode = shortcode + passkey + timestamp
        password = base64.b64encode(data_to_encode.encode()).decode()

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        payload = {
            "BusinessShortCode": shortcode,
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone,
            "PartyB": shortcode,
            "PhoneNumber": phone,
            "CallBackURL": settings.MPESA_CALLBACK_URL,
            "AccountReference": "FRUITABLES",
            "TransactionDesc": "Order Payment"
        }
        print()
        res = requests.post(
            "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest",
            json=payload, headers=headers, timeout=10)
        return res.status_code == 200

    except requests.exceptions.RequestException as e:
        print(f"Request error during STK Push: {e}")
        return False
    except ValueError as e:
        print(f"Value error during STK Push: {e}")
        return False
    except KeyError as e:
        print(f"Key error during STK Push: {e}")
        return False

@csrf_exempt
def mpesa_callback(request):
    """Mpesa callback function"""
    data = json.loads(request.body)
    print("M-Pesa Callback:", data)

    # Handle payment confirmation logic here: save to DB, update order, etc.

    return JsonResponse({"ResultCode": 0, "ResultDesc": "Received successfully"})
