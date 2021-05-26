from django.shortcuts import render
import calendar
from datetime import datetime
from django.http import JsonResponse
from .models import Appointment
from django.core.serializers.json import DjangoJSONEncoder
from django.core.serializers import serialize
from .months import MONTHS


def index(request):

    def get_date_html(day_data, month_day):
        css_classes = ['btn', 'm-2', 'date_picker_enabled date_picker_item']
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
    result_html = ''
    year = datetime.now().year
    month = datetime.now().month
    if 'month' in request.GET:
        month = int(request.GET.get('month', month))
    for day in c.itermonthdates(year, month):
        date_html = get_date_html(day, month)

        result_html += date_html
    return render(request, 'appointment/index.html', {'dates': result_html, 'month_selected': MONTHS[month-1], 'months': MONTHS})


def get_free_intervals(request):
    if 'ajax_search' in request.GET:
        appointment_list = Appointment.objects.filter(date_appointment=request.GET['picker_date'])
        data = serialize('json', appointment_list, cls=LazyEncoder)

        return JsonResponse({'appointments': data})
    else:
        return JsonResponse({'': ''})


class LazyEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Appointment):
            return str(obj)
        return super().default(obj)
