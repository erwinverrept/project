# turntable/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('turntable/', views.turntable_view, name='turntable'),
    path('', views.home_view, name='home'),

    # API endpoints die overeenkomen met de functies in views.py
    path('api/turn_by_degrees/', views.turn_by_degrees_view, name='turn_by_degrees'),
    path('api/jog/', views.jog_view, name='jog'),
]
