from core.models import Intervention
import requests

def interventions_context(request):
    return {
        'intervention': Intervention.objects.all(),
        'redirect_to': request.path
    }

def auth_status(request):
    return {
        "is_authenticated": request.user.is_authenticated
    }

def get_client_ip(request):
    """Kullanıcının IP adresini alır."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def is_from_turkey(request):
    """Kullanıcının Türkiye'den gelip gelmediğini kontrol eder ve sonucu context'e ekler."""
    if 'is_from_turkey' not in request.session:
        ip = get_client_ip(request)
        try:
            response = requests.get(f"https://ipwho.is/{ip}")
            data = response.json()
            country = data.get("country")
            is_turkey = (country == "Turkey")
        except Exception:
            is_turkey = False
        request.session['is_from_turkey'] = is_turkey

    return {
        'is_from_turkey': request.session.get('is_from_turkey', False)
    }