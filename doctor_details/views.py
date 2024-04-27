from rest_framework import status, viewsets,filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from .serializers import Ddetails_serializers,ForecastSerializer
from .models import Doctor, Patient
from .models import Forecast as Fs
from django.contrib.auth.models import User
from rest_framework.generics import GenericAPIView,RetrieveUpdateAPIView,DestroyAPIView
from django_filters import rest_framework as filter
from rest_framework.views import APIView
from rest_framework import authentication, permissions
from rest_framework.parsers import FileUploadParser
import numpy as np 
from io import BytesIO
import librosa
import pickle
import time
import matplotlib.pyplot as plt

from django.conf import settings


# ********* creating a doctor account ************* #

class d_create(GenericAPIView):
    serializer_class = Ddetails_serializers

    def post(self, request):
        # Ensure the authenticated user is retrieved properly
        user = request.user

        # Proceed only if the user is authenticated
        if user.is_authenticated:
            data = request.data
            data["user_id"] = request.user.id
            serializer = Ddetails_serializers(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({"date": serializer.data}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "User not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)
        

# ********** fetching all the enterd details in doctor ************* #
        


class d_details(APIView):
    authentication_classes=[authentication.BasicAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def get(self,request, *args, **kwargs):
        id=request.user.id
        qs=Doctor.objects.filter(user_id=id)
        serializers=Ddetails_serializers(qs,many=True)
        return Response(data=serializers.data)



# ************** update the doctor profile *************** #

class Update_Doctor(RetrieveUpdateAPIView):
    serializer_class = Ddetails_serializers
    queryset = Doctor.objects.all()

    def get_object(self):
        doctor_name = self.kwargs.get('doctor_name')  # Get the license_no from URL kwargs
        return Doctor.objects.get(doctor_name=doctor_name)  # Retrieve the doctor based on the license_no

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


# *************** delete function on Doctor ****************#
    
class Delete_Doctor(DestroyAPIView):
    serializer_class = Ddetails_serializers
    querry_set = Doctor.objects.all()

    def get_object(self):
        doctor_name = self.kwargs.get('doctor_name')
        return Doctor.objects.get(doctor_name = doctor_name)
    
    def delete (self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)





# ************** searching doctor from lsit **************** #

class Doctor_postfilter(filter.FilterSet):
    search_feilds = filter.CharFilter(field_name="Doctor name", lookup_expr="iexact")


class Search_Doctors(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = Ddetails_serializers
    filter_backends = [DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter]
    filter_class = Doctor_postfilter
    search_fields = ["doctor_name"]
    ordering_fields = "__all__"


# ************** Model prediction ***************** #




class Forecast(APIView):
    file_parser_classes = [FileUploadParser]
    def extract_features(self,y, sr):
        mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
        spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)[0]
        zcr = librosa.feature.zero_crossing_rate(y)[0]
        rmse = librosa.feature.rms(y=y)[0]
        cepstrum = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)[0]
        D = librosa.stft(y)  # Compute the spectrogram
        spectral_spread = librosa.feature.spectral_bandwidth(y=y, sr=sr)[0]


        features = np.hstack((np.mean(mfccs, axis=1), 
                          np.mean(spectral_centroid), 
                          np.mean(spectral_rolloff), 
                          np.mean(zcr), 
                          np.mean(rmse),
                          np.mean(cepstrum),
                          np.mean(spectral_spread),))
        return features
    
    def load_model(self):
        with open('resources/model.pkl', 'rb') as file:
            model = pickle.load(file)

        with open("resources/label_encoder.pkl", 'rb') as file :
            label_encoder = pickle.load(file)

        return (model, label_encoder)
    
    def get_heart_beat(self, sample, sr):
        tempo = librosa.beat.tempo(y =sample, sr=sr)
        return int(tempo[0])
    
    def spectral_centroid(self, y, sr, patient_id):

        filepath = f"media/spectral_centroid/{patient_id}_{int(time.time())}.jpeg"

        spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=sr)[0]

        frames = range(len(spectral_centroids))
        t = librosa.frames_to_time(frames)
        
        plt.figure(figsize=(6, 4))
        librosa.display.waveshow(y, sr=sr, color="r")
        plt.plot(t, spectral_centroids, color='violet', label='Spectral Centroid')
        plt.title('Waveform and Spectral Centroid')
        plt.xlabel('Time')
        plt.ylabel('Amplitude')
        plt.legend(loc='upper right')
        plt.savefig(filepath, dpi=500)

        return filepath
        
    def post(self, request, patientID):
            user = request.user
            if user.is_authenticated:
                audio_data = request.FILES["audio"]
                # file_buffer = BytesIO(audio_data)
                samples, sr = librosa.load(audio_data)
                print("********************************************")
                print("File = ", request.FILES["audio"])
                print("Sample rate = ", sr)
                print("********************************************")

                # Loading model
                model, label_encoder = self.load_model()

                input_feature_data = []
                for i in range(0, len(samples), (sr * 5)):
                    input_feature_data.append(self.extract_features(samples[i:(i + (sr * 5))], sr))

                preds = model.predict(input_feature_data)
                aggregate_class_index = round(np.mean(preds))
                forecast = label_encoder.inverse_transform([aggregate_class_index])[0]
                heart_beat = self.get_heart_beat(samples, sr) - 33
                sc_file_path = self.spectral_centroid(samples, sr, patientID)

                data_to_db = {
                    'forecast' : forecast, 
                    'heart_beat' : heart_beat, 
                    'patient' : patientID, 
                    'doctor' : Doctor.objects.get(user_id = request.user.id).id ,
                    'graph' : sc_file_path,
                    'timestamp' : int(time.time())
                            }
                
                serializer = ForecastSerializer(data=data_to_db)
                if serializer.is_valid():
                    serializer.save()

                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else :
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else :
                return Response({"error" : "user not authenticated "}, status=status.HTTP_403_FORBIDDEN)
    
    def get(self, request, patientID = 0) :
        user = (request.user)
        if user.is_authenticated :
            if Patient.objects.filter(user_id = user.id).exists():# call by patient
                data = (Fs.objects.filter(patient = Patient.objects.get(user_id = user.id).id)).order_by('-timestamp')
                serializer = ForecastSerializer(data,many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else: # call by doctor 
                data = (Fs.objects.filter(patient = patientID)).order_by('-timestamp')
                serializer = ForecastSerializer(data,many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Authentication failed" }, status=status.HTTP_403_FORBIDDEN)
