from django.shortcuts import render, get_object_or_404, redirect
import calendar
from datetime import datetime
from django.http import JsonResponse
from .models import Appointment
from django.core.serializers.json import DjangoJSONEncoder
from django.core.serializers import serialize
from .months import MONTHS


def index(request):

    year = datetime.now().year
    month = datetime.now().month

    if 'month' in request.GET:
        month = int(request.GET.get('month', month))

    date_picker_html = get_date_picker_html(year, month)

    return render(request, 'appointment/index.html',
                  {'dates': date_picker_html,
                   'month': month,
                   'month_prev': month-1,
                   'month_next': month+1,
                   'month_selected': MONTHS[month - 1],
                   })


def add_appointment(request):
    if request.method == 'GET':
        pass
    elif request.method == 'POST':
        appointment_id = request.POST['time_interval']
        year = datetime.now().year
        month = int(request.POST['month'])
        if validate(appointment_id):
            appointment = get_object_or_404(Appointment, pk=appointment_id)
            if appointment.is_booked:
                date_picker_html = get_date_picker_html(year, month)
                return render(request, 'appointment/index.html',
                              {'error_message': "Время уже занято",
                               'dates': date_picker_html,
                               'month': month,
                               'month_prev': month - 1,
                               'month_next': month + 1,
                               'month_selected': MONTHS[month - 1],
                               'last_name': request.POST['last_name'],
                               'comment': request.POST['comment'],
                               'date_of_birth': request.POST['date_of_birth']
                               })
            else:
                appointment.last_name = request.POST.get('last_name', '')
                appointment.date_of_birth = request.POST.get('date_of_birth', '')
                appointment.comment = request.POST.get('comment', '')
                appointment.is_booked = True
                appointment.save()
                return redirect('/' + str(appointment.id) + '/success/')
        else:
            date_picker_html = get_date_picker_html(year, month)
            return render(request, 'appointment/index.html', {'error_message': "Ошибка записи. Выберите дату и время!",
                                                              'dates': date_picker_html,
                                                              'month': month,
                                                              'month_prev': month - 1,
                                                              'month_next': month + 1,
                                                              'month_selected': MONTHS[month - 1],
                                                              'last_name': request.POST['last_name'],
                                                              'comment': request.POST['comment'],
                                                              'date_of_birth': request.POST['date_of_birth']
                                                              })


def validate(appointment_id):
    check = False
    if appointment_id != '':
        check = True
    return check


def success(request, appointment_id):
    appointment = get_object_or_404(Appointment, pk=appointment_id)
    return render(request, 'appointment/success.html', {
        'last_name': appointment.last_name,
        'date_appointment': appointment.date_appointment,
        'time': appointment.time_appointment, })


def get_date_picker_html(year, month):

    def get_date_html(day_data, month_day):
        css_classes = ['btn', 'date_picker_enabled', 'date_picker_item']
        append_br = ''
        disabled = ''
        if day_data.weekday() == 6 and day_data.month == month_day:
            css_classes.append('btn-outline-danger')
            append_br = '<br>'
        else:
            css_classes.append('btn-outline-primary')
        if day_data == datetime.now().date():
            css_classes.append('today')
        if day_data.month != month_day:
            css_classes.append('btn-outline-secondary')
            disabled = 'disabled'
        if day_data < datetime.now().date():
            disabled = 'disabled'
        res = '<button type="button" class="{0}" {1} value="{2}">{3}</button>{4}'.format(' '.join(css_classes),
                                                                                         disabled, day_data,
                                                                                         day_data.day, append_br, )
        return res

    c = calendar.Calendar(calendar.MONDAY)
    result_html = '<button disabled class="btn date_picker_item date_picker_day"><b>Пн</b></button>' \
                  '<button disabled class="btn date_picker_item date_picker_day"><b>Вт</b></button>' \
                  '<button disabled class="btn date_picker_item date_picker_day"><b>Ср</b></button>' \
                  '<button disabled class="btn date_picker_item date_picker_day"><b>Чт</b></button>' \
                  '<button disabled class="btn date_picker_item date_picker_day"><b>Пт</b></button>' \
                  '<button disabled class="btn date_picker_item date_picker_day"><b>Сб</b></button>' \
                  '<button disabled class="btn date_picker_item date_picker_day"><b>Вс</b></button><br>'
    for day in c.itermonthdates(year, month):
        date_html = get_date_html(day, month)

        result_html += date_html

    return result_html
