from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='ensamble'),
    path('api/run', views.run_api, name='ensamble_run'),
]
