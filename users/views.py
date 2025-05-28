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
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.urls import reverse


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

        return redirect("payment:services")
    
    return render(request, 'users/randevu.html', {})





from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.shortcuts import render

User = get_user_model()

def password_reset_view(request):
    return render(request, "users/sifremi-unuttum.html")

def password_reset_ajax(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data.get("email")
            user = User.objects.filter(email=email).first()

            if user:
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)
                reset_link = request.build_absolute_uri(
                    reverse("users:password_reset_confirm", kwargs={"uidb64": uid, "token": token})
                )

                # E-posta gönderimi
                send_mail(
                    subject="Şifre Sıfırlama",
                    message=f"Şifrenizi sıfırlamak için aşağıdaki bağlantıya tıklayın:\n{reset_link}",
                    from_email="noreply@example.com",
                    recipient_list=[email],
                )

                return JsonResponse({
                    "status": "success",
                    "message": "Şifre sıfırlama bağlantısı e-posta adresinize gönderildi."
                })

            return JsonResponse({
                "status": "error",
                "message": "Bu e-posta adresi sistemde kayıtlı değil."
            }, status=400)

        except Exception as e:
            return JsonResponse({
                "status": "error",
                "message": f"Hata oluştu: {str(e)}"
            }, status=500)



def password_reset_confirm(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (User.DoesNotExist, ValueError, TypeError, OverflowError):
        user = None

    if request.method == "POST":
        if user is not None and default_token_generator.check_token(user, token):
            try:
                data = json.loads(request.body)
                password = data.get("password")
                password2 = data.get("password2")

                if password != password2:
                    return JsonResponse({
                        "status": "error",
                        "message": "Şifreler uyuşmuyor!"
                    })

                if len(password) < 8:
                    return JsonResponse({
                        "status": "error",
                        "message": "Şifre en az 8 karakter olmalı."
                    })

                user.set_password(password)
                user.save()

                return JsonResponse({
                    "status": "success",
                    "message": "Şifreniz başarıyla güncellendi."
                })

            except Exception as e:
                return JsonResponse({
                    "status": "error",
                    "message": "Bir hata oluştu: " + str(e)
                })

        return JsonResponse({
            "status": "error",
            "message": "Bağlantı geçersiz veya süresi dolmuş."
        })

    return render(request, 'users/password_reset_confirm.html')