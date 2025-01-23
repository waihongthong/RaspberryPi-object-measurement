import paho.mqtt.client as mqtt
import json
from datetime import datetime

# MQTT Configuration
WIFI_SSID = "10.207.200.91"
WIFI_PASSWORD = "bilik703"
MQTT_BROKER = "34.59.168.251"  # Your VM instance public IP
MQTT_PORT = 1883
MQTT_TOPIC = "iot"

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode('utf-8')
        print(f"Received message: {payload}")
    except Exception as e:
        print(f"Error processing message: {e}")

def main():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    try:
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        
        # Optional: Publish a test message
        test_message = {
            "timestamp": datetime.now().isoformat(),
            "message": "Raspberry Pi MQTT Connected"
        }
        client.publish(MQTT_TOPIC, json.dumps(test_message))

        client.loop_forever()
    except Exception as e:
        print(f"Connection failed: {e}")

if __name__ == "__main__":
    main()