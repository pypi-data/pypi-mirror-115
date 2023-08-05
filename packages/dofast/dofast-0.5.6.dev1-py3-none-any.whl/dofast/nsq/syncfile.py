import json

import codefast as cf
import nsq

from .consumer import Consumer
from dofast.config import SERVER_HOST

cf.logger.level = 'info'
cf.info('Go.')


class SyncFileConsumer(Consumer):
    def __init__(self, topic: str, channel: str):

        nsq.Reader(message_handler=self.async_handler,
                   nsqd_tcp_addresses=[f'{SERVER_HOST}:4150'],
                   topic=topic,
                   channel=channel,
                   max_in_flight=10,
                   lookupd_poll_interval=3)

    def publish_message(self, message: dict):
        msg = json.loads(message.body)
        filename = msg['data']['filename']
        from dofast.oss import Bucket
        cf.info('Downloading:', filename)
        Bucket().download(filename, filename)


if __name__ == '__main__':
    SyncFileConsumer('file', 'sync').run()
