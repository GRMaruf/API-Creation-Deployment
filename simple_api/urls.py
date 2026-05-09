from django.urls import path
from simple_api.views import *

urlpatterns = [
    path('products/', product_list),
]