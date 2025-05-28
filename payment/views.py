import iyzipay
import json
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.conf import settings
import uuid
from payment.models import Service


def odeme(request):
    return render(request, "payment/checkout.html", {})


def services(request):
    all_services = Service.objects.all()

    return render(request, 'payment/services.html', {
        "services": all_services
    })