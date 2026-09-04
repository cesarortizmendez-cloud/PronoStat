from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='multiple'),
    path('api/run', views.run_api, name='multiple_run'),
]
