from django.urls import path
from . import views


app_name = 'appointment'

urlpatterns = [
    path('', views.index, name='index'),
    path('add_appointment/', views.add_appointment, name='add_appointment'),
    path('<appointment_id>/success/', views.success, name='success'),
]