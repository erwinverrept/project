# turntable/views.py
from  django.shortcuts import render
from  django.http import JsonResponse
import json
from . import laser_control

def home_view(request):
    return render(request, 'turntable/home.html')

def turntable_view(request):
    context = {'degrees': range(360)}
    return render(request, 'turntable/turntable.html', context)

def turn_by_degrees_view(request):
    """Nieuwe view voor de hoofd-draaifunctie."""
    if request.method == 'POST':
        data = json.loads(request.body)
        direction = data.get('direction')
        degrees = data.get('degrees')

        if direction in ['left', 'right'] and degrees is not None:
            new_angle = motor_control.move_by_degrees(degrees, direction)
            return JsonResponse({'status': 'success', 'new_angle': new_angle})
    
    return JsonResponse({'status': 'error'}, status=400)

def jog_view(request):
    """Nieuwe view voor de fijnafstelling (jogging)."""
    if request.method == 'POST':
        data = json.loads(request.body)
        direction = data.get('direction')
        
        if direction in ['left', 'right']:
            new_angle = motor_control.jog_motor(direction)
            return JsonResponse({'status': 'success', 'new_angle': new_angle})
            
    return JsonResponse({'status': 'error'}, status=400)
