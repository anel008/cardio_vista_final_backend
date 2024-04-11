from django.db import models
from django.contrib.auth.models import User
from patient_details.models import Patient

# Create your models here.
class Doctor(models.Model):
    doctor_name = models.CharField(max_length=50, default='DOCTOR')
    license_no = models.CharField( max_length=50,default='XXXXX')
    specialty = models.CharField(max_length=100, default='XXXXX')
    email = models.EmailField(default='example@example.com')
    phone_number = models.CharField(max_length=20, default = 0)
    bio = models.TextField(blank=True)
    #username = models.ForeignKey(User,on_delete= models.CASCADE,related_name="doctor_details",null=True)
    user_id=models.ForeignKey(User,on_delete=models.CASCADE)

class Forecast(models.Model):
    CHOICES = (
        ("healthy", "h"),
        ("un_healthy", "u")
    )
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    heart_beat = models.IntegerField()
    forecast = models.CharField(max_length=10,choices=CHOICES)
    graph = models.CharField(max_length=100)