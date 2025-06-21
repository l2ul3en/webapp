from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='reports'),
    path('hgroup/', views.hgroup, name='hgroup'),
    path('getHosts/', views.getHosts, name='getHosts'),
]