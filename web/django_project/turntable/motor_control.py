# turntable/motor_control.py
import time

try:
    import RPi.GPIO as GPIO
    IS_RASPBERRY_PI = True
except ImportError:
    print("WAARSCHUWING: RPi.GPIO kon niet worden geïmporteerd. GPIO-functionaliteit is uitgeschakeld.")
    IS_RASPBERRY_PI = False

# --- Configuratie van de Motor ---
CONTROL_PINS = [17, 18, 27, 22]
# Voor een 28BYJ-48 in 'full step' modus zijn er ~2048 stappen voor een 360 graden rotatie.
# Dit kan licht variëren, dus pas dit getal eventueel aan voor perfecte precisie.
STEPS_PER_REVOLUTION = 2048

# Stappensequentie voor 'full step'
STEP_SEQUENCE = [
    [1, 0, 0, 1], [1, 0, 0, 0], [1, 1, 0, 0], [0, 1, 0, 0],
    [0, 1, 1, 0], [0, 0, 1, 0], [0, 0, 1, 1], [0, 0, 0, 1]
]

# --- State Management (Houd de huidige positie bij) ---
# We slaan de huidige hoek op in het geheugen.
# Let op: dit reset naar 0 elke keer dat de server herstart.
current_angle = 0.0

def setup_gpio():
    if not IS_RASPBERRY_PI: return
    GPIO.setmode(GPIO.BCM)
    for pin in CONTROL_PINS:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, 0)

def _perform_steps(steps, direction):
    """Interne functie om de motor te laten draaien en de pinnen uit te schakelen."""
    if not IS_RASPBERRY_PI:
        print(f"SIMULATIE: Draai {steps} stappen naar {direction}")
        return

    sequence = STEP_SEQUENCE if direction == 'right' else STEP_SEQUENCE[::-1]
    
    for _ in range(steps):
        for step in sequence:
            for pin_index, pin_value in enumerate(step):
                GPIO.output(CONTROL_PINS[pin_index], pin_value)
            time.sleep(0.002)

    # Schakel pinnen uit om oververhitting te voorkomen
    for pin in CONTROL_PINS:
        GPIO.output(pin, 0)

def move_by_steps(steps, direction):
    """Beweeg de motor een relatief aantal stappen en update de hoek."""
    global current_angle
    _perform_steps(steps, direction)

    # Bereken de verandering in hoek en update de staat
    angle_change = (steps / STEPS_PER_REVOLUTION) * 360.0
    if direction == 'left':
        current_angle -= angle_change
    else:
        current_angle += angle_change
    
    # Zorg dat de hoek binnen 0-360 blijft
    current_angle %= 360
    return current_angle

def move_to_angle(target_angle):
    """Beweeg de motor naar een absolute hoek (0-359)."""
    global current_angle
    target_angle = float(target_angle)

    # Bereken de kortste weg om te draaien
    delta = target_angle - current_angle
    if delta > 180:
        delta -= 360
    elif delta < -180:
        delta += 360
    
    direction = 'right' if delta > 0 else 'left'
    
    # Converteer het hoekverschil naar stappen
    steps_to_move = int(abs(delta) / 360.0 * STEPS_PER_REVOLUTION)
    
    if steps_to_move > 0:
        _perform_steps(steps_to_move, direction)
    
    # Zet de hoek precies op de doelwaarde om cumulatieve fouten te voorkomen
    current_angle = target_angle
    return current_angle

# Initialiseer de GPIO pinnen wanneer de module geladen wordt
setup_gpio()
