from google.api_core import retry
from google.cloud import pubsub_v1
import logging
import lz4.block

logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)


def pull_pubsub(project_id, subscription_name, num_messages, ack=False):
    """Receives messages from a pubsub subscription."""

    subscriber = pubsub_v1.SubscriberClient()
    # The `subscription_path` method creates a fully qualified identifier
    # in the form `projects/{project_id}/subscriptions/{subscription_name}`
    subscription_path = subscriber.subscription_path(
        project_id, subscription_name)

    # The subscriber pulls a specific number of messages. The actual
    # number of messages pulled may be smaller than max_messages.
    response = subscriber.pull(
        subscription_path, max_messages=num_messages,
        retry=retry.Retry(deadline=10000),
    )

    if len(response.received_messages) == 0:
        logging.info(f"No messages received.")
        return

    ack_ids = []
    retreived_messages = []
    for received_message in response.received_messages:
        rec_m = received_message.message
        logging.info(f"Received message: {rec_m.data}.")
        if rec_m.attributes and ('compression.decompressedLength' in rec_m.attributes):
            decompressed_length = rec_m.attributes['compression.decompressedLength']
            decompressed = lz4.block.decompress(rec_m.data, uncompressed_size=int(decompressed_length))
            logging.info(f"Decompressed Received : {decompressed}.")
            retreived_messages.append(decompressed)
        else:
            logging.warning(f"Unable to decompress message: {rec_m.data}.")
            retreived_messages.append(rec_m.data)
        ack_ids.append(received_message.ack_id)

    # Acknowledges the received messages so they will not be sent again.
    if ack:
        subscriber.acknowledge(
            subscription_path, ack_ids=ack_ids
        )

    logging.info(
        f"Received {'and acknowledged ' if ack else ''}{len(response.received_messages)} message(s) from {subscription_path}."
    )

    return retreived_messages