FROM python:3.11-slim

WORKDIR /workspace

# منع الـ Python من كتابة ملفات pyc
ENV PYTHONDONTWRITEBYTECODE 1
# ضمان إرسال المخرجات مباشرة إلى شاشة العرض دون تخزين مؤقت
ENV PYTHONUNBUFFERED 1

# تثبيت الاعتمادات الأساسية للنظام
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# نسخ وتثبيت اعتمادات بايثون
COPY ./requirements.txt /workspace/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /workspace/requirements.txt

# نسخ ملفات المشروع
COPY . /workspace

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
