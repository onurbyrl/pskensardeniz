from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import CustomUser, UserProfile, Appointment
from django.db import transaction
from django.http import JsonResponse
import json


def user_login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            email = data.get('email')
            password = data.get('sifre')

            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                return JsonResponse({
                    "status": "success",
                    "message": "Giriş başarılı!",
                    "redirect_url": "/"
                })

            else:
                return JsonResponse({
                    "status": "error",
                    "message": "Geçersiz email veya şifre!"
                }, status=401)

        except Exception as e:
            return JsonResponse({
                "status": "error",
                "message": f"Giriş sırasında bir hata oluştu: {str(e)}"
            }, status=400)

    return render(request, 'users/giris-yap.html')


def register(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # JSON olarak veriyi al
            
            name = data.get('isim')
            surname = data.get('soyisim')
            email = data.get('email')
            password = data.get('sifre')
            phone = data.get('phone')
            address = data.get('adres')

            with transaction.atomic():
                # Kullanıcı oluştur
                user = CustomUser.objects.create_user(email=email, name=f"{name} {surname}", password=password)

                # Profil oluştur
                UserProfile.objects.create(
                    user=user,
                    phone_number=phone,
                    address=address
                )

                return JsonResponse({
                    "status": "success",
                    "message": "Kayıt başarılı! Giriş yapabilirsiniz.",
                    "redirect_url": "/kullanici/giris-yap/"
                })

        except Exception as e:
            return JsonResponse({
                "status": "error",
                "message": f"Kayıt sırasında bir hata oluştu: {str(e)}"
            }, status=400)

    return render(request, 'users/kayit-ol.html', {})


def user_logout(request):
    logout(request) # bakılacak
    return redirect('users:login')


def randevu_olustur(request):
    if request.method == "POST":
        date = request.POST.get("date")
        time = request.POST.get("time")
        notes = request.POST.get("notes", "")

        if not date or not time:
            return JsonResponse({"status": "error", "message": "Lütfen tüm alanları doldurun."}, status=400)

        appointment = Appointment.objects.create(
            client=request.user,  # Giriş yapmış kullanıcıyı ata
            date=date,
            time=time,
            notes=notes
        )

        return JsonResponse({"status": "success", "message": "Randevu başarıyla oluşturuldu."})
    
    return render(request, 'users/randevu.html', {})