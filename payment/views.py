import iyzipay
import json
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.conf import settings

# İyzico API bilgileri (bunları settings.py içine koyabilirsin)
IYZIPAY_API_KEY = "your_api_key"
IYZIPAY_SECRET_KEY = "your_secret_key"
IYZIPAY_BASE_URL = "https://sandbox-api.iyzipay.com"  # Test ortamı için

def create_payment(request):
    if request.method == "POST":
        # Kullanıcıdan alınan ödeme bilgileri
        user = request.user
        price = request.POST.get("price")  # Ödenecek tutar

        # İyzico API için istek verileri
        options = {
            "api_key": IYZIPAY_API_KEY,
            "secret_key": IYZIPAY_SECRET_KEY,
            "base_url": IYZIPAY_BASE_URL
        }

        payment_request = {
            "locale": "tr",
            "conversationId": "123456789",
            "price": price,
            "paidPrice": price,
            "currency": "TRY",
            "installment": 1,
            "basketId": "B67832",
            "paymentChannel": "WEB",
            "paymentGroup": "PRODUCT",
            "callbackUrl": "http://127.0.0.1:8000/payment/callback/",  # Ödeme sonucu için callback URL
            "buyer": {
                "id": str(user.id),
                "name": user.first_name,
                "surname": user.last_name,
                "email": user.email,
                "identityNumber": "11111111111",  # Test için
                "registrationAddress": "Kullanıcı Adresi",
                "city": "İstanbul",
                "country": "Turkey",
                "ip": "85.34.78.112"
            },
            "basketItems": [
                {
                    "id": "BI101",
                    "name": "Hizmet / Ürün Adı",
                    "category1": "Dijital Ürünler",
                    "itemType": "PHYSICAL",
                    "price": price
                }
            ]
        }

        # Ödeme başlatma
        payment = iyzipay.CheckoutFormInitialize().create(payment_request, options)
        payment_result = json.loads(payment.read().decode("utf-8"))

        # Kullanıcıya ödeme formunu göster
        if payment_result["status"] == "success":
            return JsonResponse({"token": payment_result["token"], "html": payment_result["checkoutFormContent"]})

        return JsonResponse({"error": "Ödeme başlatılamadı."}, status=400)

    return JsonResponse({"error": "Geçersiz istek."}, status=400)



def payment_callback(request):
    if request.method == "POST":
        token = request.POST.get("token")
        
        options = {
            "api_key": IYZIPAY_API_KEY,
            "secret_key": IYZIPAY_SECRET_KEY,
            "base_url": IYZIPAY_BASE_URL
        }

        request_data = {
            "locale": "tr",
            "conversationId": "123456789",
            "token": token
        }

        payment_result = iyzipay.CheckoutForm().retrieve(request_data, options)
        result = json.loads(payment_result.read().decode("utf-8"))

        if result["status"] == "success":
            # Ödeme başarılı -> Veritabanına kaydet
            return render(request, "payment/success.html")
        else:
            return render(request, "payment/fail.html")

    return JsonResponse({"error": "Geçersiz istek."}, status=400)
