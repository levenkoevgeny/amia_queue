from appointment.models import Appointment
from rest_framework import serializers


class AppointmentSerializer(serializers.ModelSerializer):
    time_appointment = serializers.TimeField(format="%H:%M")

    class Meta:
        model = Appointment
        fields = '__all__'