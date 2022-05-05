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

class onetSerializer(serializers.ModelSerializer):
    class Meta:
        model = onet
        fields ="__all__"

class wpSerializer(serializers.ModelSerializer):
    class Meta:
        model = wp
        fields ="__all__"

class metroprogSerializer(serializers.ModelSerializer):
    class Meta:
        model = metroprog
        fields ="__all__"

class mailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = mails
        fields ="__all__"

class raspberrySerializer(serializers.ModelSerializer):
    class Meta:
        model = raspberry
        fields ="__all__"

class modelsMLSerializer(serializers.ModelSerializer):
    class Meta:
        model = modelML
        fields ="__all__"