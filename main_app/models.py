from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

USER_TYPE = ( 
                ('Ministry_Relief', 'MINISTRY RELIEF'),
                ('City_Meyor', 'CITY MEYOR'), 
                ('District_Comissioner', 'DISTRICT COMISSIONER'), 
                ('Upazila_Officer', 'UPIZILA OFFICER'), 
                ('Upazila_Uno', 'UPAZILA UNO'),
                ('Word_Commiossioner', 'WORD COMISSIONER'),
                ('Relief_Consumer', 'RELIEF CONSUMER')
            )

class ministry_relief(models.Model):
    relief_quantity = models.IntegerField(default=0, null=False)

    nid = models.CharField(max_length=20)
    user_type = models.CharField(max_length=30, choices=USER_TYPE)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class city_meyor(models.Model):
    relief_quantity = models.IntegerField(default=0, null=False)
    contact = models.CharField(max_length=200, blank=True)
    elected_city = models.CharField(max_length=200, blank=True)

    nid = models.CharField(max_length=20)
    user_type = models.CharField(max_length=30, choices=USER_TYPE)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class district_comissioner(models.Model):
    relief_quantity = models.IntegerField(default=0, null=False)
    contact = models.CharField(max_length=200, blank=True) 
    district_name = models.CharField(max_length=200, blank=True)

    nid = models.CharField(max_length=20)
    user_type = models.CharField(max_length=30, choices=USER_TYPE)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class upazila_uno(models.Model):
    relief_quantity = models.IntegerField(default=0, null=False)
    contact = models.CharField(max_length=200, blank=True)
    area = models.CharField(max_length=200, blank=True)

    nid = models.CharField(max_length=20)
    user_type = models.CharField(max_length=30, choices=USER_TYPE)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class upazila_officer(models.Model):
    relief_quantity = models.IntegerField(default=0, null=False)
    contact = models.CharField(max_length=200, blank=True)
    upazila_name = models.CharField(max_length=200, blank=True)

    nid = models.CharField(max_length=20)
    user_type = models.CharField(max_length=30, choices=USER_TYPE)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class word_comissioner(models.Model):
    relief_quantity = models.IntegerField(default=0, null=False)
    city_name = models.CharField(max_length=200, blank=True)
    word_number = models.IntegerField(default=0, blank=True)
    contact = models.CharField(max_length=200, blank=True)

    nid = models.CharField(max_length=20)
    user_type = models.CharField(max_length=30, choices=USER_TYPE)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class relief_consumer(models.Model):
    relief_quantity = models.IntegerField(default=0, null=False)
    family_member = models.IntegerField(default=1)

    nid = models.CharField(max_length=20)
    user_type = models.CharField(max_length=30, choices=USER_TYPE)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)