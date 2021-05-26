from appointment.models import Appointment
from rest_framework import viewsets, status
from .serializers import AppointmentSerializer
from rest_framework import filters
from datetime import datetime, time


class AppointmentViewSet(viewsets.ModelViewSet):
    serializer_class = AppointmentSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['last_name', 'date_of_write']

    def get_queryset(self):
        queryset = Appointment.objects.all()
        if 'date_appointment' in self.request.query_params:
            date_appointment_req = datetime.strptime(self.request.query_params.get('date_appointment'), '%Y-%m-%d')
            if date_appointment_req == datetime.combine(datetime.today().date(), datetime.min.time()):
                time_appointment_req = datetime.strptime(self.request.query_params.get('time_appointment'),
                                                         '%H:%M:%S')
                queryset = queryset.filter(date_appointment=date_appointment_req,
                                           time_appointment__gt=time_appointment_req)
            else:
                queryset = queryset.filter(date_appointment=date_appointment_req)
        if 'is_booked' in self.request.query_params:
            is_booked_req = False if self.request.query_params.get('is_booked') == 'False' else True
            queryset = queryset.filter(is_booked=is_booked_req)
        return queryset
