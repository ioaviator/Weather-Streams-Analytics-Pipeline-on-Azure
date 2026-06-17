import sys
import time
import json
import random

from azure.eventhub import EventHubProducerClient, EventData

from config import evnt_hubs_connection_str, EVENTHUB_NAME, CITIES


# Create a producer client to send messages to the event hub
producer = EventHubProducerClient.from_connection_string(
  conn_str=evnt_hubs_connection_str, 
  eventhub_name=EVENTHUB_NAME
)


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

