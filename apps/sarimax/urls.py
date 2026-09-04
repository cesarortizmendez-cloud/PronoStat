from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='sarimax'),
    path('api/run', views.run_api, name='sarimax_run'),
]
