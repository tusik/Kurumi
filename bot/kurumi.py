# -*- coding: utf-8 -*-
import botpy
from botpy import logging, BotAPI
from botpy.message import Message

import plugins.dnd
import plugins.manager
from plugins import *
from plugins import plugin

_log = logging.get_logger()

plugin_objects = {}


def plugin_register(api: BotAPI):
    # 暂时先手动注册插件子类
    dnd = plugins.dnd.DND(api=api, )
    manager = plugins.manager.Manager(api=api)
    plugin_objects["dnd"] = dnd
    plugin_objects["manager"] = manager


class Kurumi(botpy.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        plugin_register(self.api)

    async def help(self, message: Message):
        content = "以下是现在支持的命令：\n"
        for name, plugin_object in plugin_objects.items():
            content = content + f"插件名 {name}\n"
            content = content + plugin_object.get_cmd_describe()
        await message.reply(content=content)

    async def on_at_message_create(self, message: Message):
        if '/help' in message.content:
            await self.help(message)
        else:
            for name, plugin_object in plugin_objects.items():
                for command_name, command_func in plugin_object.handlers.items():
                    if command_name in message.content:
                        params = message.content.split(command_name)[1].strip()
                        await command_func["function"](plugin_object, message=message, params=params)
