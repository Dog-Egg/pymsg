import json
import threading
import time
from collections import deque
from collections.abc import Iterable
from itertools import chain

import requests

__all__ = ['DingTalkRobot', 'SendFailure']


def _prepend(value, iterable):
    return chain([value], iterable)


class SendFailure(Exception):
    pass


class DingTalkRobot:
    _instances = {}
    _cls_lock = threading.Lock()
    _t: float

    def __new__(cls, webhook, *args, **kwargs):
        with cls._cls_lock:
            if webhook not in cls._instances:
                self = super().__new__(cls)
                self._webhook = webhook
                self._t = 0
                self._queue = deque()
                self._lock = threading.Lock()

                cls._instances[webhook] = self
            return cls._instances[webhook]

    @property
    def webhook(self):
        return self._webhook

    def _send(self, data):
        try:
            response = requests.post(self._webhook, json=data)
        except Exception as exc:
            raise SendFailure(exc) from exc

        try:
            content = response.json()
        except json.JSONDecodeError:
            return False
        else:
            errcode, errmsg = content['errcode'], content['errmsg']
            # 0: ok
            # 130101: send too fast
            if errcode not in (0, 130101):
                raise SendFailure(errmsg)
            return errcode == 0

    def send(self, data=None):
        with self._lock:
            if data is not None:
                self._queue.append(data)

            if self._t < time.time():
                while self._queue:
                    if self._send(self._queue[0]):
                        self._queue.popleft()
                    else:
                        self._t = time.time() + 60
                        break
            return len(self._queue)

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
        return self.send(data)

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
        return self.send(data)

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
        return self.send(data)

    def action_card(self, title, text, btn, *btns, btns_vertically=True, hide_avatar=False):
        if not btns:
            btns = {'singleTitle': btn[0], 'singleURL': btn[1]}
        else:
            btns = {'btns': [{'title': b[0], 'actionURL': b[1]} for b in _prepend(btn, btns)]}
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
        return self.send(data)

    def feed_card(self, card, *cards):
        data = {
            "feedCard": {
                "links": [
                    {
                        "title": c[0],
                        "messageURL": c[1],
                        "picURL": c[2]
                    } for c in _prepend(card, cards)
                ]
            },
            "msgtype": "feedCard"
        }
        return self.send(data)
