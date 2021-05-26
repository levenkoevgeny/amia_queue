import django_filters
from appointment.models import Appointment
from django import forms


class AppointmentFilter(django_filters.FilterSet):
    date_appointment = django_filters.DateFilter(field_name='date_appointment',
                                                 widget=forms.DateInput(
                                                     attrs={
                                                         'type': 'date'
                                                     }))
    last_name = django_filters.CharFilter(lookup_expr='icontains')

    ordering = django_filters.OrderingFilter(
        # tuple-mapping retains order
        fields=(
            ('last_name', 'last_name'),
            ('date_of_birth', 'date_of_birth'),
            ('date_of_write', 'date_of_write'),
        ),
    )

    class Meta:
        model = Appointment
        fields = ['date_appointment', 'last_name', 'is_booked']
