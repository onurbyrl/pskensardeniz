from django.shortcuts import render, redirect, get_object_or_404
from .models import Intervention, Message, Article
from django.http import JsonResponse
import json
import requests



def get_client_ip(request):
    """Kullanıcının IP adresini alır."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def index(request):
    interventions = Intervention.objects.all()
    country = ""
    ip = get_client_ip(request)
    
    ip = "163.230.138.140"
    print("USER IP: ", ip)
    try:
        response = requests.get(f"https://ipwho.is/{ip}")
        data = response.json()
        country = data.get("country")
        print("Detected country: ", country)
        is_turkey = (country == "Turkey")
    except Exception as e:
        print("Country detection error: ", e)
        is_turkey = False
    request.session['is_from_turkey'] = is_turkey

    print("country: ", country)

    return render(request, 'pages/index.html', {
        "interventions": interventions
    })


def search_results(request):
    query = request.GET.get("search_query", "").strip()
    results = Intervention.objects.none()  # Varsayılan olarak boş sonuç

    if query:
        results = Intervention.objects.filter(title__icontains=query) | Intervention.objects.filter(description__icontains=query)

    return render(request, "search_results.html", {"query": query, "results": results})



def uygulama_detay(request, slug):
    intervention = get_object_or_404(Intervention, slug=slug)
    return render(request, 'pages/uygulama.html', {'intervention': intervention})


def iletisim(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            name = data.get("name", "")
            phone = data.get("phone", "")
            email = data.get("email", "")
            subject = data.get("subject", "")
            message = data.get("message", "")

            Message.objects.create(
                name=name,
                phone=phone,
                email=email,
                subject=subject,
                message=message
            )

            return JsonResponse({
                "status": "success",
                "message": "En kısa sürede mail adresinize dönüş yapılacaktır",
                "redirect_url": "/"
            })
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})
    
    return render(request, 'pages/iletisim.html', {})


def hakkimizda(request):
    return render(request, 'pages/hakkimizda.html', {})


def ilkelerimiz(request):
    return render(request, 'pages/ilkelerimiz.html', {})


def blog(request):
    Articles = Article.objects.all()

    return render(request, 'pages/blog.html', {
        "articles": Articles
    })


def article_detay(request, slug):
    article = get_object_or_404(Article, slug=slug)
    return render(request, 'pages/article.html', {'article': article})


