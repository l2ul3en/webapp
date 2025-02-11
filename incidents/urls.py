from django.urls import path
from . import views

urlpatterns = [
    path('', views.index , name='incidents'),
    #path('servicenow/', views.servicenow , name='servicenow'),
]
