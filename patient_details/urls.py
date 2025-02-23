from django.urls import path
from .views import p_create,p_details,Update_Patient,Delete_patient,recordings,p_names
from doctor_details.views import Search_Doctors,d_details

urlpatterns = [

    #************PATIENT***********#
    path('pd',p_details.as_view()),   # view patient detail
    path('p_namelist',p_names.as_view()), # view patients name list
    path('Pupdate/<str:name>',Update_Patient.as_view()),   # update the patient details
    path('Pdelete/<str:name>',Delete_patient.as_view()),   # delete patient
    path('Pcreate',p_create.as_view()),   # create the patient details
    path('record',recordings.as_view()),   # recordings save to DataBase
    #path('p/<str:pk>/',views.p_details),


    #*************DOCTOR IN PATIENT *************#


    path('Dsearch',Search_Doctors.as_view({'get':'list'})), # search the doctors
    path('d',d_details.as_view()),  # view the doctor details
    
    
]