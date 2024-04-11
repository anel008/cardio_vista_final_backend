from rest_framework.serializers import ModelSerializer
from .models import Patient
from doctor_details.models import Forecast
from rest_framework import serializers



class pdetails_serializers(ModelSerializer):
    # other = serializers.CharField(max_length=50, allow_blank=True)
    class Meta:
        model = Patient
        fields = ['name','dob','phone_number','age','weight','height','sex','hyper_tension_bp','chest_pain','palpitation','surgery','other','user_id']

class recording_serializers(ModelSerializer):

    class Meta:
        model = Forecast
        fields = '__all__'


class patient_name_list_serializers(ModelSerializer):
    class Meta:
        model = Patient
        fields = ['name']
