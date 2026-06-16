import os
import sys
import time
import json
import random
from dotenv import load_dotenv
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
from azure.eventhub import EventHubProducerClient, EventData


load_dotenv()

KEY_VAULT_NAME=os.getenv('KEY_VAULT_NAME')
key_vault_url = f"https://{KEY_VAULT_NAME}.vault.azure.net"

credential = DefaultAzureCredential()
kv_secret_client = SecretClient(vault_url=key_vault_url, credential=credential)

event_hubs_conn_str_frm_kv = 'event-hubs-conn-str'
evnt_hubs_connection_str = kv_secret_client.get_secret(event_hubs_conn_str_frm_kv).value


# Event Hubs event hub store name
EVENTHUB_NAME = 'evnt_hub_store'

# Create a producer client to send messages to the event hub
producer = EventHubProducerClient.from_connection_string(
  conn_str=evnt_hubs_connection_str, 
  eventhub_name=EVENTHUB_NAME
)

# Expanded list of cities with latitudes and longitudes
CITIES = [
  {"city": "New York", "latitude": 40.7128, "longitude": -74.0060},
  {"city": "Los Angeles", "latitude": 34.0522, "longitude": -118.2437},
  {"city": "Chicago", "latitude": 41.8781, "longitude": -87.6298},
  {"city": "Houston", "latitude": 29.7604, "longitude": -95.3698},
  {"city": "Miami", "latitude": 25.7617, "longitude": -80.1918},
  {"city": "Seattle", "latitude": 47.6062, "longitude": -122.3321},
  {"city": "Denver", "latitude": 39.7392, "longitude": -104.9903},
  {"city": "San Francisco", "latitude": 37.7749, "longitude": -122.4194},
  {"city": "London", "latitude": 51.5074, "longitude": -0.1278},
  {"city": "Paris", "latitude": 48.8566, "longitude": 2.3522},
  {"city": "Berlin", "latitude": 52.5200, "longitude": 13.4050},
  {"city": "Tokyo", "latitude": 35.6895, "longitude": 139.6917},
  {"city": "Beijing", "latitude": 39.9042, "longitude": 116.4074},
  {"city": "Sydney", "latitude": -33.8688, "longitude": 151.2093},
  {"city": "Cape Town", "latitude": -33.9249, "longitude": 18.4241},
  {"city": "Dubai", "latitude": 25.276987, "longitude": 55.296249},
  {"city": "São Paulo", "latitude": -23.5505, "longitude": -46.6333},
  {"city": "Toronto", "latitude": 43.6532, "longitude": -79.3832},
  {"city": "Moscow", "latitude": 55.7558, "longitude": 37.6173},
  {"city": "Mumbai", "latitude": 19.0760, "longitude": 72.8777}
]

def generate_weather_data():
  """Generate simulated weather data including latitude and longitude."""
  location = random.choice(CITIES)  # Pick a random city
  
  return {
      "city": location["city"],
      "latitude": location["latitude"],
      "longitude": location["longitude"],
      "temperature": round(random.uniform(-20.0, 45.0), 2),  # °C
      "humidity": round(random.uniform(5.0, 100.0), 2),  # %
      "wind_speed": round(random.uniform(0.0, 50.0), 2),  # km/h
      "pressure": round(random.uniform(950.0, 1050.0), 2),  # hPa
      "precipitation": round(random.uniform(0.0, 50.0), 2),  # mm
      "cloud_cover": round(random.uniform(0.0, 100.0), 2),  # %
      "weather_condition": random.choice(["Sunny", "Cloudy", "Rainy", "Stormy", "Snowy", "Foggy", "Windy", "Hazy"]),
      "timestamp": time.strftime('%Y-%m-%d %H:%M:%S')  # ISO-like timestamp
  }

try:
  while True:
    # Create a batch of events
    event_data_batch = producer.create_batch()

    # Generate sample weather data
    weather_data = generate_weather_data()

    # Format the message as JSON
    message = json.dumps(weather_data)

    # Add the JSON-formatted message to the batch
    event_data_batch.add(EventData(message))

    # Send the batch of events to Event Hubs
    producer.send_batch(event_data_batch)

    print(f"Sent: {message}")

    # Wait before sending the next reading
    time.sleep(3) 

except KeyboardInterrupt:
  print("Stopped by the user")
  sys.exit(130)

except Exception as e:
  print(f"Error: {e}")
  sys.exit(1)

finally:
  if producer is not None:
    producer.close()

