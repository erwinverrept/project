# laser/views.py
from django.shortcuts import render
from django.http import JsonResponse
import json
from . import laser_control

def laser_view(request):
        """Rendert de hoofdpagina voor de laserbediening."""
        return render(request, 'laser/laser.html')

def set_laser_state_view(request):
        """API view om de staat van de laser te veranderen."""
        if request.method == 'POST':
            data = json.loads(request.body)
            state = data.get('state', False) # True voor 'aan', False voor 'uit'
            
            laser_control.set_laser(state)
            
            status_text = "aan" if state else "uit"
            return JsonResponse({'status': 'success', 'message': f'Laser is nu {status_text}'})
            
        return JsonResponse({'status': 'error', 'message': 'Alleen POST requests zijn toegestaan.'}, status=400)
    