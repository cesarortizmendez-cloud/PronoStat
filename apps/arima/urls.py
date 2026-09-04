from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='arima'),
    path('api/run', views.run_api, name='arima_run'),
    path('api/auto', views.auto_api, name='arima_auto'),
    path('api/rolling', views.rolling_api, name='arima_rolling'),
]
