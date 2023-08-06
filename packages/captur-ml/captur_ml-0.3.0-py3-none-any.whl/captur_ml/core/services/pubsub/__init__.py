import json

from captur_ml.core.exceptions import GoogleCloudPubSubTopicDoesNotExistError
from google.cloud import pubsub_v1
from google.api_core import exceptions as google_exceptions


def publish(
    payload: dict,
    topic_name: str,
    project_name: str = "capturpwa",
    publisher: pubsub_v1.PublisherClient = None,
):
    """Publishes a message to a Pub/Sub topic.

    Args:
        payload (dict): Jsonlike message to be published.
        topic_name (str): Name of the Pub/Sub topic to publish to.
        project_name (str, optional): The GCP project name. Defaults to "capturpwa".
        publisher (pubsub_v1.PublisherClient, optional): The Publisher Client. Defaults to None.

    Raises:
        `captur_ml.core.exceptions.GoogleCloudPubSubTopicDoesNotExistError`: Raised if the topic is not found.
    """
    if publisher is None:
        publisher = pubsub_v1.PublisherClient()

    data = json.dumps(payload).encode("utf-8")

    topic_path = publisher.topic_path(project_name, topic_name)

    future = publisher.publish(topic_path, data)

    try:
        future.result()
    except google_exceptions.NotFound:
        raise GoogleCloudPubSubTopicDoesNotExistError()


def test_topic_permissions(
    project_id,
    topic_id,
    client: pubsub_v1.PublisherClient = None,
):
    if client is None:
        client = pubsub_v1.PublisherClient()
    topic_path = client.topic_path(project_id, topic_id)

    permissions_to_check = ["pubsub.topics.publish", "pubsub.topics.update"]

    allowed_permissions = client.test_iam_permissions(
        request={"resource": topic_path, "permissions": permissions_to_check}
    )

    print(
        "Allowed permissions for topic {}: {}".format(topic_path, allowed_permissions)
    )
