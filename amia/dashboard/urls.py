from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required


app_name = 'dashboard'

urlpatterns = [
    path('', login_required(views.dashboard_main), name='main'),
    path('queue_create/', login_required(views.dashboard_queue_create), name='queue_create'),
]