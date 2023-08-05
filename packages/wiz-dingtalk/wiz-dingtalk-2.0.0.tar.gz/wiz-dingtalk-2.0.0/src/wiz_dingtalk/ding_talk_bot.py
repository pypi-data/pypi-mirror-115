# _*_ coding:utf-8 _*_
import base64
import hashlib
import hmac
import json
import logging
import time

import requests
from wiz_message.bot_client import BotClient
from wiz_message.message import Message, TextMessage, MarkdownMessage
from wiz_utils.string_utils import StringUtils


class DingTalkBot(BotClient):
    base_url = "https://oapi.dingtalk.com/robot/send"

    def __init__(self, webhook, secret: str = None):
        super().__init__(webhook, secret)

    @classmethod
    def filter(cls, webhook: str):
        return "dingtalk.c" in webhook

    def convert_message(self, message: Message):
        if isinstance(message, TextMessage):
            if message.title is None or message.content is None:
                raise AttributeError("title or content is null")
            return json.dumps({"msgtype": "text", "text": {"title": message.title, "content": message.content}})
        elif isinstance(message, MarkdownMessage):
            if message.title is None or message.content is None:
                raise AttributeError("title or content is null")
            return json.dumps({"msgtype": "markdown", "markdown": {"title": message.title, "text": message.content}})

    def send_message(self, message: Message):
        return self.send(message)

    def send(self, message: Message = None, json_message: str = None):
        ts = int(time.time() * 1000)
        params = {"timestamp": ts}
        if StringUtils.is_not_blank(self.secret_key):
            string_to_sign = "%s\n%s" % (ts, self.secret_key)
            sign = base64.b64encode(hmac.new(self.secret_key.encode("utf-8"), string_to_sign.encode("utf-8"),
                                             digestmod=hashlib.sha256).digest())
            params['sign'] = sign
        try:
            request_body = self.convert_message(message) if message is not None else json_message
            if StringUtils.is_blank(request_body):
                raise AttributeError("request body is null")
            response = requests.post(url=self.webhook, params=params,
                                     headers={"Content-Type": "application/json; charset=utf-8"}, data=request_body)
            print(response.content)
        except Exception as e:
            logging.error("send message error", e)
