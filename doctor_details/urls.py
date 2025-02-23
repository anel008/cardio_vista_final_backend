from django.urls import path
from .views import d_create,d_details,Update_Doctor,Delete_Doctor,Forecast#,p_create #,DoctorUpdateDelete,Search_Doctors
from patient_details.views import p_create,Search_Patient,p_details,Update_Patient,Delete_patient



urlpatterns = [
    
    #***********DOCTOR**********#
    
    path('dc',d_create.as_view()),  #doctor create
    path('dd',d_details.as_view()), #doctor details
    path('Dupdate/<str:doctor_name>',Update_Doctor.as_view()),   #update doctor
    path('Ddelete/<str:doctor_name>',Delete_Doctor.as_view()),   #Delete doctor
    path("forecast", Forecast.as_view()),   # model training - give audio file <= 2 mb as input
    # path('result',result.as_view()),
    

    #**********PATIENT IN DOCTOR **********#

    path('pd',p_details.as_view()),     #patient detail view
    path('pc',p_create.as_view()),      #patient create
    path('Pupdate/<str:name>',Update_Patient.as_view()),     #update the patient details
    path('Pdelete/<str:name>',Delete_patient.as_view()),     #delete patient
    path('Psearch',Search_Patient.as_view({'get':'list'}))   #patient search 

]
