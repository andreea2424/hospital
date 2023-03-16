from asyncio import AbstractServer
from django.db import models
from rest_framework import serializers
from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import AbstractUser


class Assistant(models.Model):
    id = models.IntegerField(primary_key=True)
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    name = models.CharField(max_length=255)

class Treatment(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255,default="none")
    description = models.TextField(default="none")
    def __str__(self):
        return self.description

class Patient(models.Model):
    id = models.AutoField(primary_key=True)
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    name = models.CharField(max_length=255)
    age = models.IntegerField()
    gender = models.CharField(max_length=255)
    treatment = models.ManyToManyField(Treatment, through='Prescription')
    assistants = models.ManyToManyField(Assistant, through='Assignment')
    
class Doctor(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor',null=True, blank=True)
    name = models.CharField(max_length=255)
    specialty = models.CharField(max_length=255)
    patients = models.ManyToManyField(Patient, related_name='doctors')

class Assignment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    assistant = models.ForeignKey(Assistant, on_delete=models.CASCADE)
    assigned_date = models.DateTimeField(auto_now_add=True)
     
class Prescription(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    treatment= models.ForeignKey(Treatment, on_delete=models.CASCADE)
    assigned_date = models.DateTimeField(auto_now_add=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

class TreatmentApplied(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    treatment= models.ForeignKey(Treatment, on_delete=models.CASCADE)
    assistant = models.ForeignKey(Assistant, on_delete=models.CASCADE)
    date_applied = models.DateTimeField(auto_now_add=True)
    drug = models.CharField(max_length=255)
    dosage = models.FloatField()

