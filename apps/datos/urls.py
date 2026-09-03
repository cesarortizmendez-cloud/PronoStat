from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='datos'),
    path('api/analyze', views.analyze_api, name='datos_analyze'),
    path('api/clean', views.clean_api, name='datos_clean'),
]
