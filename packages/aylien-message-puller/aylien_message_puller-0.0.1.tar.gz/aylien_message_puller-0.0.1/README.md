aylien-message-puller
===============

Google Cloud provides emulators for testing PubSub. Here you will find a tool that will pull messages for subscriptions taking project ID, subscription ID and the maximum number of messages as input.

The retreived messages can be acknowledged using the flag 'ack' (which is turned off by default).

Install using pip (Python 3):

```
pip install aylien-message-puller
```

### Example

To pull messages from a subscription, you will need to provide the project-id, subscription-id, and the maximum number of messages

```
import aylien_message_puller
aylien_message_puller.pull_pubsub("project-id", "subscription-id", 10)
```

The default mechanisn does not  the received messages are not acknowledged. However, if you would like to acknowledge them, set the flag as true.

```
import aylien_message_puller
aylien_message_puller.pull_pubsub("project-id", "subscription-id", 10, true)
```