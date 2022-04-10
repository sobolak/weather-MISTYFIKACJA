from django.db.models import fields
from rest_framework import serializers
from .models import *

class interiaSerializer(serializers.ModelSerializer):
    class Meta:
        model = interia
        fields ="__all__"

class avenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = avenue
        fields ="__all__"

class weatherChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = weatherChannel
        fields ="__all__"