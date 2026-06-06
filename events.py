import os
from azure.eventhub import EventHubProducerClient, EventData
from dotenv import load_dotenv

load_dotenv()

# Event Hubs connection string and event hub name
CONNECTION_STR = os.getenv('CONNECTION_STR')
EVENTHUB_NAME = 'evnt_hub_store'

# Create a producer client to send messages to the event hub
producer = EventHubProducerClient.from_connection_string(conn_str=CONNECTION_STR, eventhub_name=EVENTHUB_NAME)

print(dir(producer))
