# API-Creation-Deployment
Basic api creation in django and deployment in cPanal

# 1. What is an API?

API = a way for applications to communicate using data.

Example:

Your frontend sends request:

```text id="2k4hm4"
GET /api/products/
```

Django returns JSON:

```json id="0oq7h0"
[
  {
    "id": 1,
    "name": "Laptop",
    "price": 50000
  }
]
```

---

# 2. Install Django REST Framework

Inside your Django project:

```bash id="t66gpb"
pip install djangorestframework
```

Add to `settings.py`

```python id="4jx0bz"
INSTALLED_APPS = [
    ...
    'rest_framework',
]
```

---

# 3. Create app

```bash id="h9suvm"
python manage.py startapp api
```

Add app:

```python id="0wy44v"
INSTALLED_APPS = [
    ...
    'api',
]
```

---

# 4. Create model

Inside `api/models.py`

```python id="4t2t3v"
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()

    def __str__(self):
        return self.name
```

---

# 5. Migrate database

```bash id="plnt9i"
python manage.py makemigrations
python manage.py migrate
```

---

# 6. Create serializer

Serializer converts model ↔ JSON.

Create:

```text id="9ot8ta"
api/serializers.py
```

Add:

```python id="ot0x7j"
from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
```

---

# 7. Create API view

Inside `api/views.py`

```python id="gg4lkk"
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Product
from .serializers import ProductSerializer

@api_view(['GET'])
def product_list(request):

    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)

    return Response(serializer.data)
```

---

# 8. Create URLs

Create:

```text id="z9gq2k"
api/urls.py
```

Add:

```python id="rk95ib"
from django.urls import path
from .views import product_list

urlpatterns = [
    path('products/', product_list),
]
```

---

# 9. Main URL config

Inside main `urls.py`

```python id="w8yx4h"
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
]
```

---

# 10. Run server

```bash id="5i9r4y"
python manage.py runserver
```

Now visit:

```text id="p0ah6q"
http://127.0.0.1:8000/api/products/
```

You’ll see JSON.

---

# 11. Add data from admin

Register model in `admin.py`

```python id="9utdko"
from django.contrib import admin
from .models import Product

admin.site.register(Product)
```

Create superuser:

```bash id="omhrd4"
python manage.py createsuperuser
```

Login:

```text id="my2otm"
http://127.0.0.1:8000/admin/
```

Add products.

Refresh API URL.

---

# 12. POST API (Create Data)

Update `views.py`

```python id="ijyrpt"
@api_view(['GET', 'POST'])
def product_list(request):

    if request.method == 'GET':
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)
```

Now you can:

* GET products
* POST products

---

# 13. Example POST request

Using Postman:

POST:

```text id="04k8bz"
http://127.0.0.1:8000/api/products/
```

JSON:

```json id="szx6jg"
{
  "name": "Phone",
  "price": 20000
}
```

---

# 14. Better version using DRF generics

Later learn:

```python id="q2k97g"
ListCreateAPIView
RetrieveUpdateDestroyAPIView
```

These reduce code massively.

---

# 15. Basic Deployment on cPanel

Now deployment.

---

# Step 1 — Prepare requirements

Inside project:

```bash id="c7cezq"
pip freeze > requirements.txt
```

---

# Step 2 — Push project to GitHub

Upload:

* project
* requirements.txt

Do NOT upload:

* venv
* db.sqlite3
* **pycache**

---

# Step 3 — Login to cPanel

Open:

* File Manager
* Setup Python App

---

# Step 4 — Create Python app

In cPanel:

## Setup Python App

Choose:

* Python version
* Application root

Example:

```text id="b6cc6u"
/home/username/myapi
```

Application startup file:

```text id="6ttt2k"
passenger_wsgi.py
```

Application Entry point:

```text id="ksk7j3"
application
```

Create app.

---

# Step 5 — Open terminal in cPanel

Activate environment:

```bash id="iv04xf"
source /home/username/virtualenv/myapi/3.11/bin/activate
```

Install requirements:

```bash id="krb1wq"
pip install -r requirements.txt
```

---

# Step 6 — Configure passenger_wsgi.py

Replace content:

```python id="1sn9q1"
import os
import sys

sys.path.insert(0, "/home/username/myapi")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project_name.settings")

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
```

Replace:

* username
* project_name

---

# Step 7 — ALLOWED_HOSTS

In `settings.py`

```python id="nv8c4y"
ALLOWED_HOSTS = [
    'yourdomain.com',
]
```

---

# Step 8 — Static files

Add:

```python id="7up4vb"
STATIC_ROOT = BASE_DIR / 'staticfiles'
```

Run:

```bash id="4fyg7p"
python manage.py collectstatic
```

---

# Step 9 — Migrate

```bash id="zg0s6u"
python manage.py migrate
```

---

# Step 10 — Restart application

In cPanel:

* Setup Python App
* Restart

---

# 16. Test API

Visit:

```text id="ihavmo"
https://yourdomain.com/api/products/
```

If working → deployment successful.

---

# Recommended Next Learning

After this learn:

1. Serializer validation
2. Authentication
3. JWT
4. CRUD APIs
5. Permissions
6. Class-based views
7. ViewSets
8. Deployment with PostgreSQL
9. Nginx + Gunicorn + VPS
10. Docker

Those are the real backend developer skills.
