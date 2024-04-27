from rest_framework.serializers import ModelSerializer
from .models import Patient
from doctor_details.models import Forecast
from rest_framework import serializers



class pdetails_serializers(ModelSerializer):
    class Meta:
        model = Patient
        fields = "__all__"

class recording_serializers(ModelSerializer):

    class Meta:
        model = Forecast
        fields = '__all__'


class patient_name_list_serializers(ModelSerializer):
    class Meta:
        model = Patient
        fields = ['name']
