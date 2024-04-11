from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.



class Patient(models.Model):
    name = models.CharField(max_length=100, default='patient')
    dob = models.DateField(default=timezone.now)
    phone_number = models.IntegerField( default='0')
    age = models.IntegerField(default=0)  # Changed to IntegerField
    weight = models.IntegerField(default=0)  
    height = models.IntegerField(default=0)  

    SEX_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    sex = models.CharField(max_length=1, choices=SEX_CHOICES)

    hyper_tension_bp = models.BooleanField(default=False)  # Default added
    chest_pain = models.BooleanField(default=False) # Default added
    palpitation = models.BooleanField(default=False) # Default added
    surgery = models.BooleanField(default=False)  # Default added
    other = models.TextField(max_length=50, default='')  # Default added

    user_id=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
