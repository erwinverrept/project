# turntable/views.py
from django.shortcuts import render
from django.http import JsonResponse
import json
from . import motor_control

def home_view(request):
    return render(request, 'turntable/home.html')

def turntable_view(request):
    context = {'degrees': range(360)}
    return render(request, 'turntable/turntable.html', context)

def move_stepper_view(request):
    """View voor de 'Draai links/rechts' knoppen."""
    if request.method == 'POST':
        data = json.loads(request.body)
        direction = data.get('direction')
        # Stappen per klik, bv. voor fijne afstelling
        steps = int(data.get('steps', 20))
        
        new_angle = motor_control.move_by_steps(steps, direction)
        return JsonResponse({'status': 'success', 'new_angle': new_angle})
    
    return JsonResponse({'status': 'error'}, status=405)

def set_angle_view(request):
    """NIEUWE View om de motor op een absolute hoek te zetten."""
    if request.method == 'POST':
        data = json.loads(request.body)
        target_angle = data.get('angle')

        if target_angle is not None:
            new_angle = motor_control.move_to_angle(target_angle)
            return JsonResponse({'status': 'success', 'new_angle': new_angle})
    
    return JsonResponse({'status': 'error'}, status=405)
