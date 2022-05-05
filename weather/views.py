from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import * 
from .models import *
from datetime import date, timedelta
from itertools import chain

# Create your views here.

@api_view(['GET'])
def apiStart(request):
    api_urls = {
        '----------------------1':'1----------------------',
        '----------------------2':'2----------------------',
        '----------------------3':'3----------------------', 
        '----------------------4':'4----------------------'
		}
    return Response(api_urls)

@api_view(['GET'])
def interiaAll(request,r):
    records = interia.objects.filter(region = r)
    selectedDay = date.today()

    records1 = records.filter(weather_time = selectedDay)
    selectedDay = selectedDay + timedelta(days=1)
    records2 = records.filter(weather_time = selectedDay)
    selectedDay = selectedDay + timedelta(days=1)
    records3 = records.filter(weather_time = selectedDay)
    selectedDay = selectedDay + timedelta(days=1)
    records4 = records.filter(weather_time = selectedDay)
    selectedDay = selectedDay + timedelta(days=1)
    records5 = records.filter(weather_time = selectedDay)
    selectedDay = selectedDay + timedelta(days=1)
    records6 = records.filter(weather_time = selectedDay)
    result = list(chain(records1, records2, records3, records4, records5, records6))

    serializer = interiaSerializer(result, many = True  )
    return Response(serializer.data)

@api_view(['GET'])
def avenueAll(request,r):
    records = avenue.objects.filter(region = r)
    selectedDay = date.today()
    
    records1 = records.filter(weather_time = selectedDay)
    selectedDay = selectedDay + timedelta(days=1)
    records2 = records.filter(weather_time = selectedDay)
    selectedDay = selectedDay + timedelta(days=1)
    records3 = records.filter(weather_time = selectedDay)
    
    result = list(chain(records1, records2, records3))
    serializer = avenueSerializer(result, many = True  )
    return Response(serializer.data)

@api_view(['GET'])
def weatherChannelAll(request,r):
    records = weatherChannel.objects.filter(region = r)
    selectedDay = date.today()

    records1 = records.filter(weather_time = selectedDay)
    selectedDay = selectedDay + timedelta(days=1)
    records2 = records.filter(weather_time = selectedDay)
    selectedDay = selectedDay + timedelta(days=1)
    records3 = records.filter(weather_time = selectedDay)

    result = list(chain(records1, records2, records3))
    serializer = weatherChannelSerializer(result, many = True  )
    return Response(serializer.data)

@api_view(['GET'])
def onetAll(request,r):
    records = onet.objects.filter(region = r)
    selectedDay = date.today()

    records1 = records.filter(weather_time = selectedDay)
    selectedDay = selectedDay + timedelta(days=1)
    records2 = records.filter(weather_time = selectedDay)
    selectedDay = selectedDay + timedelta(days=1)
    records3 = records.filter(weather_time = selectedDay)

    result = list(chain(records1, records2, records3))
    serializer = onetSerializer(result, many = True  )
    return Response(serializer.data)

@api_view(['GET'])
def wpAll(request,r):
    records = wp.objects.filter(region = r)
    selectedDay = date.today()

    records1 = records.filter(weather_time = selectedDay)
    selectedDay = selectedDay + timedelta(days=1)
    records2 = records.filter(weather_time = selectedDay)
    selectedDay = selectedDay + timedelta(days=1)
    records3 = records.filter(weather_time = selectedDay)

    result = list(chain(records1, records2, records3))
    serializer = wpSerializer(result, many = True  )
    return Response(serializer.data)

@api_view(['GET'])
def metroprogAll(request,r):
    records = metroprog.objects.filter(region = r)
    selectedDay = date.today()

    records1 = records.filter(weather_time = selectedDay)
    selectedDay = selectedDay + timedelta(days=1)
    records2 = records.filter(weather_time = selectedDay)
    selectedDay = selectedDay + timedelta(days=1)
    records3 = records.filter(weather_time = selectedDay)

    result = list(chain(records1, records2, records3))
    serializer = metroprogSerializer(result, many = True  )
    return Response(serializer.data)

@api_view(['GET'])
def raspAll(request):
    records = raspberry.objects.all().order_by('-id')[:12]
    serializer = raspberrySerializer(records, many = True)

    return Response(serializer.data)

@api_view(['GET'])
def modelMLAll(request):
    records = modelML.objects.all().order_by('-id')[:12]
    serializer = modelsMLSerializer(records, many = True)

    return Response(serializer.data)

@api_view(['POST'])
def mailsAdd(request):
    serializer = mailsSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)