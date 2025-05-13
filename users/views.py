from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import CustomUser, UserProfile, Appointment
from django.db import transaction
from django.http import JsonResponse
import json
from datetime import datetime
from django.utils.timezone import make_aware
from django.contrib.auth.decorators import login_required
from pytz import timezone


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


@login_required
def user_profile(request):
    user = request.user
    now = datetime.now()

    # Geçmiş randevular
    past_appointments = Appointment.objects.filter(client=user, date__lt=now.date()).order_by('-date', '-time')

    # Gelecek randevular
    future_appointments = Appointment.objects.filter(client=user, date__gte=datetime.now().date()).order_by('date', 'time')

    return render(request, 'users/profil.html', {
        'past_appointments': past_appointments,
        'future_appointments': future_appointments
    })


@login_required
def user_logout(request):
    logout(request) # bakılacak
    return redirect('users:login')


def randevu_olustur(request):
    if request.method == "POST":
        date = request.POST.get("date")
        time = request.POST.get("time")
        notes = request.POST.get("notes", "")
        timezone_str = request.POST.get("timezone", "Europe/Istanbul")

        if not date or not time:
            return JsonResponse({"status": "error", "message": "Lütfen tüm alanları doldurun."}, status=400)

        turkey_tz = timezone('Europe/Istanbul')
        client_tz = timezone(request.POST.get('timezone'))  # formdan gelirse

        datetime_str = f"{request.POST.get('date')} {request.POST.get('time')}"
        client_dt = client_tz.localize(datetime.strptime(datetime_str, "%Y-%m-%d %H:%M"))
        turkey_dt = client_dt.astimezone(turkey_tz)
        print("türkiye saatiyle: ", turkey_dt)

        # Aynı zamanda başka randevu var mı kontrolü
        from users.models import Appointment
        exists = Appointment.objects.filter(date=turkey_dt.date(), time=turkey_dt.time()).exists()

        if exists:
            return JsonResponse({
                "status": "error",
                "message": "Bu saat için zaten bir randevu mevcut. Lütfen başka bir saat seçin."
            }, status=400)

        # Randevuyu oluştur
        Appointment.objects.create(
            client=request.user,
            date=turkey_dt.date(),
            time=turkey_dt.time(),
            notes=notes
        )

        return redirect("payment:checkout")
    
    return render(request, 'users/randevu.html', {})