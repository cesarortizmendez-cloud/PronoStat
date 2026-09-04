from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='inferencia'),
    path('api/ic-media', views.ic_media_api, name='inferencia_ic_media'),
    path('api/ic-prop', views.ic_prop_api, name='inferencia_ic_prop'),
    path('api/n-media', views.n_media_api, name='inferencia_n_media'),
    path('api/n-prop', views.n_prop_api, name='inferencia_n_prop'),
]
