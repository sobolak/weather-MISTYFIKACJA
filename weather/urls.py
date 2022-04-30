from django import views
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.apiStart, name="start"),
    path('interia/<str:r>', views.interiaAll, name="interia"),
    path('avenue/<str:r>', views.avenueAll, name="avenue"),
    path('weatherChannel/<str:r>', views.weatherChannelAll, name="weatherChannel"),
    path('onet/<str:r>', views.onetAll, name="onet"),
    path('wp/<str:r>', views.wpAll, name="wp"),
    path('metroprog/<str:r>', views.metroprogAll, name="metroprog"),
    path('mailsAdd', views.mailsAdd, name="mailsAdd"),
]