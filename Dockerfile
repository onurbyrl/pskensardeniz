# 1. Temel Python imajını al
FROM python:3.10

# 2. Ortam değişkenleri
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 3. Sistem kütüphanelerini yükle
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 4. Çalışma dizinini oluştur
WORKDIR /app

# 5. Gerekli dosyaları kopyala
COPY requirements.txt /app/

# 6. Bağımlılıkları yükle
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# 7. Proje dosyalarını kopyala
COPY . /app/

# 8. Statik dosyaları topla (deployment öncesi)
RUN python manage.py collectstatic --noinput

# 9. Uygulama başlatıcı komut
CMD ["gunicorn", "pskensar.wsgi:intervention", "--bind", "0.0.0.0:8000"]
