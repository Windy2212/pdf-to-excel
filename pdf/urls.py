from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view,name='homepage'),
    path('upload/', views.pdf_view,name='upload'),
]
