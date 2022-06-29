from django.urls import path
from .views import index, explore

urlpatterns = [
    path('', index),
    path('explore/<id>', explore, name="explore")
]