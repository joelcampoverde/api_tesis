from django.urls import path
from .views import *

urlpatterns = [
    path('process_command/', process_command, name='process_command'),
]