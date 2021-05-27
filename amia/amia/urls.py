from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest import views

router = routers.DefaultRouter()
router.register(r'appointments', views.AppointmentViewSet, basename='Appointment')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('appointment.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('rest/', include(router.urls)),
    path('accounts/', include('django.contrib.auth.urls'))
]
