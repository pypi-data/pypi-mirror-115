#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""The ``pubsub`` module facilitates interacting with Pub/Sub streams by
publishing, pulling subscriptions, and decoding alert streams.
"""

from fastavro import reader
from google.cloud import pubsub_v1
from io import BytesIO
import logging
import os
import pandas as pd
from typing import Optional, Union


pgb_project_id = 'ardent-cycling-243415'

###--- Publish and pull ---#
def publish(topic_name, message, project_id=pgb_project_id, attrs={}):
    """Publish encoded messages to a Pub/Sub topic.
    Wrapper for `publish` from `pubsub_v1`.

    Args:
        topic_name  (str): The Pub/Sub topic name for publishing alerts
        message     (bytes): The message to be published
        attts       (dict): Message attributes to be published
    """

    publisher = pubsub_v1.PublisherClient()

    topic_path = publisher.topic_path(project_id, topic_name)

    # topic = publisher.get_topic(topic_path)
    # log.info(f'Connected to PubSub: {topic_path}')

    future = publisher.publish(topic_path, data=message, **attrs)

    return future.result()

def pull(subscription, max_messages: int = 1, project_id: Optional[str] = None, msg_only: bool = True):
    """Pull and acknowledge a fixed number of messages from a Pub/Sub topic.

    Wrapper for the synchronous
    `google.cloud.pubsub_v1.SubscriberClient().pull()`

    Args:
        subscription: The Pub/Sub subcription to pull from.

        max_messages: The maximum number of messages to pull.

        project_id: GCP project ID for the project containing the subscription.
                    If None, the environment GOOGLE_CLOUD_PROJECT will be used.

        msg_only: Whether to return the full packet or just the message contents.

    Returns:
        A list of messages
    """
    if project_id is None:
        project_id = os.getenv('GOOGLE_CLOUD_PROJECT')

    # setup for pull
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project_id, subscription)
    request = {
        "subscription": subscription_path,
        "max_messages": max_messages,
    }

    # wrap in 'with' block to automatically call close() when done
    with subscriber:

        # pull
        response = subscriber.pull(**request)

        # unpack the messages
        message_list, ack_ids = [], []
        for received_message in response.received_messages:
            if msg_only:
                message_list.append(received_message.message.data)  # bytes
            else:
                message_list.append(received_message)
            ack_ids.append(received_message.ack_id)

        # acknowledge the messages so they will not be sent again
        ack_request = {
            "subscription": subscription_path,
            "ack_ids": ack_ids,
        }
        subscriber.acknowledge(**ack_request)

    return message_list

def streamingPull(subscription, callback, project_id=None, timeout=10):
    """Pull and acknowledge messages from a Pub/Sub topic continuously (streaming).

    Wrapper for the asynchronous
    `google.cloud.pubsub_v1.SubscriberClient().subscribe()`

    Args:
        subscription: The Pub/Sub subcription to pull from.

        max_messages: The maximum number of messages to pull.

        project_id: GCP project ID for the project containing the subscription.
                    If None, the environment GOOGLE_CLOUD_PROJECT will be used.

        msg_only: Whether to return the full packet or just the message contents.

    Returns:
        A list of messages
    """
    if project_id is None:
        project_id = os.getenv('GOOGLE_CLOUD_PROJECT')

    with pubsub_v1.SubscriberClient() as subscriber:
        subscription_path = subscriber.subscription_path(project_id, subscription)
        streaming_pull_future = subscriber.subscribe(subscription_path, callback)
        try:
            streaming_pull_future.result(timeout=timeout)
        except TimeoutError:
            streaming_pull_future.cancel()  # Trigger the shutdown.
            streaming_pull_future.result()  # Block until the shutdown is complete.

    # return streaming_pull_future

###--- Subscribe to a PGB stream from an external account ---###
def subscribe(topic: str, project_id: Optional[str] = None, subscription: Optional[str] = None):
    """Create a subscription in the account associated with `project_id`
    to the requested Pitt-Google Broker topic.
    Wrapper for `google.cloud.pubsub_v1.SubscriberClient().create_subscription()`

    ?? The user's machine must already be configured with a GCP service account key
    and associated enviornment variables.

    Args:

        topic: Name of a Pitt-Google Broker Pub/Sub topic to subscribe to.

        project_id: User's GCP project ID. If None, the environment variable
                    GOOGLE_CLOUD_PROJECT will be used. The subscription will be
                    created in this account.

        subscription: Name for the user's Pub/Sub subscription. If None,
                      `topic` will be used.

    """
    if project_id is None:
        project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
    if subscription is None:
        subscription = topic

    subscriber = pubsub_v1.SubscriberClient()
    publisher = pubsub_v1.PublisherClient()

    sub_path = subscriber.subscription_path(project_id, subscription)
    topic_path = publisher.topic_path(pgb_project_id, topic)

    sub = subscriber.create_subscription(sub_path, topic_path)

    print(f'Created subscription {sub.name}')
    print(f'attached to topic {sub.topic}')

    return sub

###--- Decode alert data ---###

def decode_ztf_alert(msg, return_format='dict', strip_cutouts=False):
    """Decode alert bytes using fastavro and return in requested format.
    Args:
        msg (pubsub message): single ZTF alert
    """

    # Extract the alert data from msg -> dict
    with BytesIO(msg) as fin:
        alertDicts = [r for r in reader(fin)]  # list of dicts

    # ZTF alerts are expected to contain one dict in this list
    assert (len(alertDicts) == 1)
    alert_dict = alertDicts[0]

    if strip_cutouts:
        alert_dict = strip_cutouts_ztf(alert_dict)

    if return_format == 'dict':
        return alert_dict
    elif return_format == 'df':
        return alert_dict_to_dataframe(alert_dict)

def strip_cutouts_ztf(alertDict):
    """
    Args:
        alertDict (dict): ZTF alert formated as a dict
    Returns:
        alertStripped (dict): ZTF alert dict with the cutouts (postage stamps) removed
    """
    cutouts = ['cutoutScience', 'cutoutTemplate', 'cutoutDifference']
    alertStripped = {k:v for k, v in alertDict.items() if k not in cutouts}
    return alertStripped

def alert_dict_to_dataframe(alert_dict: dict) -> pd.DataFrame:
    """ Packages an alert into a dataframe.
    Adapted from: https://github.com/ZwickyTransientFacility/ztf-avro-alert/blob/master/notebooks/Filtering_alerts.ipynb
    """
    dfc = pd.DataFrame(alert_dict['candidate'], index=[0])
    df_prv = pd.DataFrame(alert_dict['prv_candidates'])
    dflc = pd.concat([dfc,df_prv], ignore_index=True)

    # we'll attach some metadata--note this may not be preserved after all operations
    # https://stackoverflow.com/questions/14688306/adding-meta-information-metadata-to-pandas-dataframe
    dflc.objectId = alert_dict['objectId']
    dflc.candidate = alert_dict['candid']
    return dflc
