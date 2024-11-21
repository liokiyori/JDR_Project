from django.urls import path
from . import views

urlpatterns = [
    path('', views.forum_homes, name='forum_home'),
]