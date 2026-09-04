from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='econometria'),
    path('api/ols', views.ols_api, name='econometria_ols'),
]
