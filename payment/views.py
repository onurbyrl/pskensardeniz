import iyzipay
import json
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.conf import settings
import uuid


def odeme(request):
    return render(request, "payment/checkout.html", {})