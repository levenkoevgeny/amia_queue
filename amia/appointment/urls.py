from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required


app_name = 'appointment'

urlpatterns = [
    path('', views.index, name='index'),
    path('get-free-intervals/', views.get_free_intervals, name='get_free_intervals'),
]