# laser/urls.py
from django.urls import path
from . import views

urlpatterns = [
        # De hoofdpagina voor de laser app (bv. /laser/)
        path('', views.laser_view, name='laser_home'),
        
        # De API endpoint om de laser aan/uit te zetten (bv. /laser/api/set_state/)
        path('api/set_state/', views.set_laser_state_view, name='set_laser_state'),
    ]
    