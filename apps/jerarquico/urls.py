from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='jerarquico'),
    path('api/run', views.run_api, name='jerarquico_run'),
]
