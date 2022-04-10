from django import views
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.apiStart, name="start"),
    path('interia/<str:r>', views.interiaAll, name="interiaAll"),
    path('avenue/<str:r>', views.avenueAll, name="avenueAll"),
    path('weatherChannel/<str:r>', views.weatherChannelAll, name="weatherChannel"),
]