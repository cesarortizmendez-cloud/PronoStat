from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='simulacion'),
    path('api/run', views.run_api, name='simulacion_run'),
]
