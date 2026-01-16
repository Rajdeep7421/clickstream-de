# data_generator/src/eventhub_publisher.py

import json
from azure.eventhub import EventHubProducerClient, EventData
from src import config

class EventHubPublisher:
    """
    Handles connection to Azure Event Hubs and publishing of events.
    """
    def __init__(self):
        """Initializes the Event Hubs producer client."""
        if not config.EVENTHUB_CONNECTION_STR or not config.EVENTHUB_NAME:
            raise ValueError("Event Hubs connection string or name not configured. Check .env and src/config.py")

        self.producer = EventHubProducerClient.from_connection_string(
            conn_str=config.EVENTHUB_CONNECTION_STR,
            eventhub_name=config.EVENTHUB_NAME
        )

        eventhub_connection_string_filtered = config.EVENTHUB_CONNECTION_STR.replace("Endpoint=", "").split(";")[0]
        print(f"Initialized Event Hub Publisher for: {config.EVENTHUB_NAME} in namespace: {eventhub_connection_string_filtered}")

    def publish_events(self, events):
        """
        Publishes a list of events to Event Hubs in a single batch.
        Args:
            events (list): A list of Python dictionaries, where each dict is an event.
        """
        if not events:
            return

        event_data_batch = self.producer.create_batch()
        for event in events:
            try:
                event_data_batch.add(EventData(json.dumps(event)))
            except ValueError as e:
                print(f"Warning: Event too large for batch, sending current batch and starting new one. Error: {e}")
                self.producer.send_batch(event_data_batch) # Send current batch
                event_data_batch = self.producer.create_batch() # Start new batch
                event_data_batch.add(EventData(json.dumps(event))) # Add current event to new batch

        self.producer.send_batch(event_data_batch) # Send the final batch
        return len(events) 

    def close(self):
        """Closes the Event Hubs producer connection."""
        self.producer.close()
        print("Event Hub Producer closed.")