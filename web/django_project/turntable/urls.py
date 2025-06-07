# turntable/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('turntable/', views.turntable_view, name='turntable'),
    path('', views.home_view, name='home'),

    # NIEUWE URL voor de motorbesturing
    path('api/move_stepper/', views.move_stepper_view, name='move_stepper'),
]
