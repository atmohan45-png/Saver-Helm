import requests
import time
import random
import sys

# Configuration
API_URL = "http://127.0.0.1:5000/api/data"
HELMET_IDS = ["H001", "H002", "H003"]

print("Starting ESP32 Data Simulation...")
print(f"Targeting: {API_URL}")
print("Press Ctrl+C to stop.")

try:
    while True:
        for h_id in HELMET_IDS:
            temp = round(25.0 + random.uniform(0, 10), 1)
            gas = random.randint(300, 800)
            battery = random.randint(15, 100)
            
            payload = {
                "helmet_id": h_id,
                "temperature": temp,
                "gas": gas,
                "battery": battery
            }
            
            try:
                response = requests.post(API_URL, json=payload)
                if response.status_code in [201, 200]:
                    status = "DANGER" if gas > 650 else "SAFE"
                    print(f"[{time.strftime('%H:%M:%S')}] Send Success: {h_id} | Temp: {temp}C | Gas: {gas} | Status: {status}")
                else:
                    print(f"[{time.strftime('%H:%M:%S')}] Failed: {h_id} - Response: {response.status_code}")
            except Exception as e:
                print(f"Error connecting to server: {e}")
                sys.exit(1)
                
        time.sleep(5)

except KeyboardInterrupt:
    print("\nSimulation stopped.")
