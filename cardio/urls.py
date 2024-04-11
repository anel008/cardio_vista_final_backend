from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('patient_details/',include('patient_details.urls')),
    path('accounts/',include('accounts.urls')),
    path('doctor_details/',include('doctor_details.urls'))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)