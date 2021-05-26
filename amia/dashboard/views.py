from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from appointment.models import Appointment
from datetime import datetime, time, timedelta

from dashboard.filters import AppointmentFilter


def dashboard_main(request):
    f = AppointmentFilter(request.GET, queryset=Appointment.objects.all().order_by('date_appointment',
                                                                                   'time_appointment'))
    paginator = Paginator(f.qs, 100)
    page = request.GET.get('page')
    items = paginator.get_page(page)
    return render(request, 'dashboard/dashboard_main.html', {'appointment_list': items,
                                                             'filter': f,
                                                             })


def dashboard_queue_create(request):
    if request.method == 'POST':
        if validate_data():

            Appointment.objects.all().delete()
            date_from = datetime.strptime(request.POST['date_from'], '%Y-%m-%d')
            date_till = datetime.strptime(request.POST['date_till'], '%Y-%m-%d')
            work_day_from = int(request.POST['work_day_from'])
            work_day_till = int(request.POST['work_day_till'])
            time_interval = int(request.POST['time_interval'])

            time_intervals = get_time_intervals(work_day_from, work_day_till, time_interval)
            dates_for_appointments = get_dates(date_from, date_till)

            for date_f_a in dates_for_appointments:
                for time_inter in time_intervals:
                    appointment = Appointment(
                        date_appointment=date_f_a,
                        time_appointment=time_inter
                    )
                    appointment.save()
            return HttpResponseRedirect(reverse('dashboard:main'))
    else:
        return render(request, 'dashboard/queue_input_form.html')


def validate_data(data=None):
    return True


def get_minute_intervals(time_interval):
    def time_range(start, end, delta):
        current = start
        while current < end:
            yield current
            current += delta

    dts = [dt for dt in time_range(0, 60, time_interval)]
    return dts


def get_time_intervals(work_day_from, work_day_till, time_interval):
    minutes_intervals = get_minute_intervals(time_interval)
    time_intervals = []
    for hour in range(work_day_from, work_day_till):
        for minutes in minutes_intervals:
            t = time(hour, minutes)
            time_intervals.append(t)
    return time_intervals


def get_dates(date_from, date_till):
    def date_range(start, end, delta):
        current = start
        while current <= end:
            yield current
            current += delta

    dates = [d for d in date_range(date_from, date_till, timedelta(days=1))]
    return dates