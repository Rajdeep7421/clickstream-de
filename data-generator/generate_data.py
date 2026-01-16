# data_generator/generate_data.py

import time
import random
from src import config
from src.event_generator import generate_clickstream_event
from src.eventhub_publisher import EventHubPublisher

def main():
    """
    Main function to run the clickstream data generator.
    """
    publisher = None
    try:
        publisher = EventHubPublisher()
        print("Starting clickstream data generator. Press Ctrl+C to stop.")

        while True:
            events_to_send = []
            num_events_in_batch = random.randint(1, config.MAX_EVENTS_PER_BATCH)
            for _ in range(num_events_in_batch):
                event = generate_clickstream_event()
                events_to_send.append(event)
                # print(events_to_send)

            if events_to_send:
                sent_count = publisher.publish_events(events_to_send)
                print(f"Sent {sent_count} events.")

            time.sleep(config.SLEEP_INTERVAL_SECONDS)

    except KeyboardInterrupt:
        print("\nStopping data generator gracefully...")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        if publisher:
            publisher.close()

if __name__ == "__main__":
    main()