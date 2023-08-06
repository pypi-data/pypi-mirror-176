# -*- coding: utf-8 -*-

from __future__ import absolute_import
from builtins import object
import os
import logging
import json

from google.cloud import pubsub_v1

LOGGER = logging.getLogger(__name__)


class Publisher(object):
    topic_name = None

    def __init__(self, topic_id):
        self.instance = pubsub_v1.PublisherClient()
        self.topic_name = 'projects/{project_id}/topics/{topic}'.format(
            project_id=os.getenv('PUBSUB_PUBLISHER_PROJECT_ID'),
            topic=topic_id,
        )

    def publish(self, body, raise_exception=False, retry_connection=0, **kwargs):
        LOGGER.info('Publishing message %s, %s', body, kwargs)

        future = self.instance.publish(
            self.topic_name, json.dumps(body).encode('utf-8'), **kwargs)

        def handle_publish_done(future):
            try:
                future.result()
            except Exception as e:
                LOGGER.warning('Message not published')

                if retry_connection > 0:
                    self.publish(body, raise_exception, retry_connection - 1)
                else:
                    if raise_exception:
                        raise e

        future.add_done_callback(handle_publish_done)
