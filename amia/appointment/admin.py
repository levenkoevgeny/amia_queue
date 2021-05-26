from django.contrib import admin
from .models import *


@admin.register(Appointment)
class AppointmentPageAdmin(admin.ModelAdmin):
    list_display = ('date_appointment', 'time_appointment', 'last_name', 'date_of_birth', 'email', 'date_of_write', 'is_booked', 'comment')
    list_filter = ('is_booked',)
    search_fields = ['last_name']
    list_editable = ('is_booked',)
