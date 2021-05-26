from django.forms import ModelForm
from appointment.models import Appointment


class AppointmentForm(ModelForm):

    class Meta:
        model = Appointment
        fields = ['last_name', 'comment', 'is_booked', 'email']