from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='probabilidad'),
    path('api/fit', views.fit_api, name='probabilidad_fit'),
    path('api/normalidad', views.normalidad_api, name='probabilidad_normalidad'),
    path('api/prob', views.prob_api, name='probabilidad_prob'),
]
