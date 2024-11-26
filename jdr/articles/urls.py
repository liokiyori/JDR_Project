from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.list_article, name="list_article"),
]