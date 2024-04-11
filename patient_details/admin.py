from django.contrib import admin
from .models import Patient
from  doctor_details.models import Forecast



# Register your models here.
admin.site.register(Patient)
admin.site.register(Forecast)
# admin.site.register(Doctor_details)
