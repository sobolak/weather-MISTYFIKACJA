from django.db import models

# Create your models here.

class interia(models.Model):
    id = models.AutoField(primary_key = True)
    temperature = models.IntegerField()
    wind = models.IntegerField()
    humidity = models.IntegerField()
    rain = models.FloatField()
    cloudiness = models.IntegerField()
    update_time = models.CharField(max_length=50)
    weather_time = models.CharField(max_length=20)
    hour = models.IntegerField()
    region = models.CharField(max_length=20)
    class Meta:
        managed = False
        db_table = 'interia'


class avenue(models.Model):
    id = models.AutoField(primary_key = True)
    temperature = models.IntegerField()
    wind = models.IntegerField()
    humidity = models.IntegerField()
    rain = models.FloatField()
    cloudiness = models.IntegerField()
    update_time = models.CharField(max_length=50)
    weather_time = models.CharField(max_length=20)
    hour = models.IntegerField()
    region = models.CharField(max_length=20)
    class Meta:
        managed = False
        db_table = 'avenue'


class weatherChannel(models.Model):
    id = models.AutoField(primary_key = True)
    temperature = models.IntegerField()
    wind = models.IntegerField()
    humidity = models.IntegerField()
    rain = models.FloatField()
    cloudiness = models.IntegerField()
    update_time = models.CharField(max_length=50)
    weather_time = models.CharField(max_length=20)
    hour = models.IntegerField()
    region = models.CharField(max_length=20)
    class Meta:
        managed = False
        db_table = 'weatherChannel'

class onet(models.Model):
    id = models.AutoField(primary_key = True)
    temperature = models.IntegerField()
    wind = models.IntegerField()
    humidity = models.IntegerField()
    rain = models.FloatField()
    cloudiness = models.IntegerField()
    update_time = models.CharField(max_length=50)
    weather_time = models.CharField(max_length=20)
    hour = models.IntegerField()
    region = models.CharField(max_length=20)
    class Meta:
        managed = False
        db_table = 'onet'

class wp(models.Model):
    id = models.AutoField(primary_key = True)
    temperature = models.IntegerField()
    wind = models.IntegerField()
    humidity = models.IntegerField()
    rain = models.FloatField()
    cloudiness = models.IntegerField()
    update_time = models.CharField(max_length=50)
    weather_time = models.CharField(max_length=20)
    hour = models.IntegerField()
    region = models.CharField(max_length=20)
    class Meta:
        managed = False
        db_table = 'wp'

class metroprog(models.Model):
    id = models.AutoField(primary_key = True)
    temperature = models.IntegerField()
    wind = models.IntegerField()
    humidity = models.IntegerField()
    rain = models.FloatField()
    cloudiness = models.IntegerField()
    update_time = models.CharField(max_length=50)
    weather_time = models.CharField(max_length=20)
    hour = models.IntegerField()
    region = models.CharField(max_length=20)
    class Meta:
        managed = False
        db_table = 'metroprog'