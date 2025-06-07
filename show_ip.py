import socket
import fcntl
import struct
import time
from datetime import datetime
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306

# --- Configuratie van het OLED-display ---
# Stel de I2C interface in
# Controleer of het I2C adres 0x3C is, dit is het meest voorkomende adres voor SSD1306 displays.
# Soms kan het ook 0x3D zijn. Je kunt dit controleren met 'i2cdetect -y 1'
serial = i2c(port=1, address=0x3C) # De '1' verwijst naar I2C bus 1 op de Raspberry Pi

# Initialiseer het SSD1306 OLED-apparaat
device = ssd1306(serial)

# --- Functies om netwerkinformatie op te halen ---

def get_ip_address(ifname):
    """Haalt het IP-adres op van een opgegeven netwerkinterface."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Gebruik fcntl.ioctl om de SIOCGIFADDR (get interface address) te roepen
        # Dit werkt op Linux-systemen om netwerkinformatie op te halen.
        return socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915,  # SIOCGIFADDR
            struct.pack('256s', ifname[:15].encode('utf-8'))
        )[20:24])
    except OSError:
        return None # Interface niet gevonden of geen IP-adres toegewezen

def has_internet_connection():
    """Controleert of er een actieve internetverbinding is door te pingen naar Google DNS."""
    try:
        # Probeer een verbinding te maken met een bekende externe host (Google DNS)
        # Een korte timeout om niet te lang te wachten.
        socket.create_connection(("8.8.8.8", 53), timeout=1)
        return True
    except OSError:
        return False

# --- Hoofdloop van het script ---
print("OLED IP-adres display script gestart. Druk op Ctrl+C om af te sluiten.")

try:
    while True:
        # Haal het IP-adres op van de Wi-Fi interface (wlan0) of Ethernet (eth0)
        # Pas dit aan afhankelijk van je verbindingsmethode
        ip_addr = get_ip_address('wlan0')
        if ip_addr is None:
            ip_addr = get_ip_address('eth0')

        # Controleer of er een internetverbinding is
        internet_active = has_internet_connection()

        # Render de tekst op het OLED-display
        with canvas(device) as draw:
            draw.text((0, 0), "Rpi Status:", fill="white")
            draw.line((0, 10, device.width, 10), fill="white") # Een lijn onder de titel

            if internet_active:
                draw.text((0, 20), "Internet: Online", fill="white")
                if ip_addr:
                    draw.text((0, 35), f"IP: {ip_addr}", fill="white")
                else:
                    draw.text((0, 35), "IP: N.v.t. (geen)", fill="white")
            else:
                draw.text((0, 20), "Internet: Offline", fill="white")
                draw.text((0, 35), "Geen IP-adres", fill="white")

            # Optioneel: Toon de huidige tijd
            current_time = datetime.now().strftime("%H:%M:%S")
            draw.text((0, 50), f"Tijd: {current_time}", fill="white")

        time.sleep(5) # Wacht 5 seconden voordat je het IP-adres opnieuw controleert

except KeyboardInterrupt:
    print("\nScript afgesloten door gebruiker.")
    # Optioneel: Wis het scherm bij afsluiten
    with canvas(device) as draw:
        draw.text((0, 0), "Uitschakelen...", fill="white")
    time.sleep(1)
    device.clear() # Wis het scherm volledig
except Exception as e:
    print(f"Er is een fout opgetreden: {e}")
    device.clear() # Wis het scherm bij een fout