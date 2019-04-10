import json
import logging
import threading
import time
from collections.abc import Iterable
from queue import Queue
from pprint import pformat

import requests

__all__ = ['DingTalkRobot']


class DingTalkRobot:
    _instances = {}

    def __new__(cls, webhook, *args, **kwargs):
        k = hash(webhook)
        if k not in cls._instances:
            cls._instances[k] = super().__new__(cls)
        return cls._instances[k]

    def __init__(self, webhook):
        if not getattr(self, '_inited', False):
            self._inited = True
            self._webhook = webhook
            self._t = time.time()
            self._cache_q = Queue(20)
            self._mutex = threading.Lock()

            logger = logging.getLogger('DingTalkRobot(%s)' % self._webhook[-7:])
            logger.setLevel(logging.INFO)
            handler = logging.StreamHandler()
            handler.setFormatter(logging.Formatter('[%(levelname)s %(asctime)s %(name)s] %(message)s', '%F %H:%M:%S'))
            logger.addHandler(handler)
            self.logger = logger

    @property
    def webhook(self):
        return self._webhook

    def set_cache_size(self, size):
        if not isinstance(size, int):
            raise TypeError('require an integer')
        self._cache_q.maxsize = size

    def _http_post(self, data):
        response = requests.post(self._webhook, json=data)
        self.logger.debug('response body: %s' % response.text)
        try:
            content = json.loads(response.content)
        except json.JSONDecodeError:
            return False
        else:
            return content['errmsg'] == 'ok' and content['errcode'] == 0

    def _send(self, data):
        if self._http_post(data):
            return True
        else:
            self._t = time.time() + 60
            return False

    def _msg_queue(self, data):
        with self._mutex:
            if self._t < time.time():
                can_send = True

                while can_send and not self._cache_q.empty():
                    if self._send(self._cache_q.queue[0]):
                        self._cache_q.get_nowait()
                    else:
                        can_send = False

                if not can_send or not self._send(data):
                    self._add_to_cache(data)
            else:
                self._add_to_cache(data)

    def _add_to_cache(self, data):
        if self._cache_q.full():
            self.logger.warning('消息发送频率过高，缓存队列已满，该消息丢失\t%s' % pformat(data))
        else:
            self._cache_q.put_nowait(data)
            self.logger.info('消息已加入缓存队列\t%s' % pformat(data))

    def text(self, content, at=None, at_all=False):
        data = {
            "msgtype": "text",
            "text": {
                "content": content
            },
            "at": {
                "atMobiles": self._format_at(at),
                "isAtAll": at_all
            }
        }
        self._msg_queue(data)

    @staticmethod
    def _format_at(at):
        if isinstance(at, Iterable) and not isinstance(at, str):
            return [str(x) for x in at]
        return [] if at is None else [str(at)]

    def link(self, title, text, msg_url, pic_url=''):
        data = {
            "msgtype": "link",
            "link": {
                "text": text,
                "title": title,
                "picUrl": pic_url,
                "messageUrl": msg_url
            }
        }
        self._msg_queue(data)

    def markdown(self, title, text, at=None, at_all=False):
        data = {
            "msgtype": "markdown",
            "markdown": {
                "title": title,
                "text": text
            },
            "at": {
                "atMobiles": self._format_at(at),
                "isAtAll": at_all
            }
        }
        self._msg_queue(data)

    def action_card(self, title, text, btn, *btns, btns_vertically=True, hide_avatar=False):
        if not len(btns):
            btns = {'singleTitle': btn[0], 'singleURL': btn[1]}
        else:
            btns = {'btns': [{'title': b[0], 'actionURL': b[1]} for b in [btn] + list(btns)]}
        data = {
            "actionCard": {
                "title": title,
                "text": text,
                "hideAvatar": "1" if hide_avatar else "0",
                "btnOrientation": "0" if btns_vertically else "1",
                **btns,
            },
            "msgtype": "actionCard"
        }
        self._msg_queue(data)

    def feed_card(self, card, *cards):
        cards = [card] + list(cards)
        data = {
            "feedCard": {
                "links": [
                    {
                        "title": c[0],
                        "messageURL": c[1],
                        "picURL": c[2]
                    } for c in cards
                ]
            },
            "msgtype": "feedCard"
        }
        self._msg_queue(data)
