# -*- coding: utf-8 -*-
import botpy
from botpy import logging, BotAPI

from botpy.ext.command_util import Commands
from botpy.message import Message

_log = logging.get_logger()

@Commands("跑团", "dnd")
async def dnd(api: BotAPI, message: Message, params=None):
    _log.info(params)
    content = f"你好，{message.author.username}，你的参数是：{params}"
    # 第一种用reply发送消息
    await message.reply(content=params)
    return True

class Kurumi(botpy.Client):
    async def on_at_message_create(self, message: Message):
        # 注册指令handler
        handlers = [
            dnd,
        ]
        for handler in handlers:
            if await handler(api=self.api, message=message):
                return