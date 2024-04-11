from rest_framework.serializers import ModelSerializer
from .models import Doctor
from patient_details.models import Patient

class Ddetails_serializers(ModelSerializer):
    class Meta :
        model = Doctor
        fields = '__all__'
        #extra_kwargs = {"username":{"read_only" : True}}



# class health_serializer(ModelSerializer):
#     class Meta :
#         model = health
#         fields = '__all__'


class result_serializers(ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['name']

