# -*- coding: utf-8 -*-
import botpy
from botpy import logging, BotAPI
from botpy.message import Message, GroupMessage

import plugins.dnd
import plugins.manager
import plugins.weather
import plugins.latex
import plugins.chat
from bot.message import KurumiMessage
from plugins import *
from plugins import plugin
from bot.core import BotCore

_log = logging.get_logger()

bot_core = BotCore()


def plugin_register(api: BotAPI):
    # 暂时先手动注册插件子类
    dnd = plugins.dnd.DND(bot_core, api=api)
    manager = plugins.manager.Manager(bot_core, api=api)
    weather = plugins.weather.Weather(bot_core, api=api)
    latex = plugins.latex.Latex(bot_core, api=api)
    chat = plugins.chat.Chat(bot_core, api=api)
    bot_core.plugin_objects["dnd"] = dnd
    bot_core.plugin_objects["manager"] = manager
    bot_core.plugin_objects["weather"] = weather
    bot_core.plugin_objects["latex"] = latex
    bot_core.plugin_objects["main"] = chat


class Kurumi(botpy.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        plugin_register(self.api)

    def set_config(self, config):
        self.config = config
        bot_core.config = config

    def set_script_path(self, path):
        bot_core.script_path = path

    async def help(self, message: Message):
        content = "以下是现在支持的命令：\n"
        for name, plugin_object in bot_core.plugin_objects.items():
            content = content + f"插件名 {name}\n"
            content = content + plugin_object.get_cmd_describe()
        await message.reply(content=content)

    async def help_in_group(self, message: GroupMessage):
        content = "以下是现在支持的命令：\n"
        for name, plugin_object in bot_core.plugin_objects.items():
            content = content + f"插件名 {name}\n"
            content = content + plugin_object.get_cmd_describe()
        await self.api.post_group_message(group_openid=message.group_openid,
                                          msg_type=0,
                                          msg_id=message.id,
                                          content=content)

    async def on_group_at_message_create(self, message: GroupMessage):
        if bot_core.me["channel"] is None:
            bot_core.me["channel"] = await self.api.me()

        if '/help' in message.content:
            await self.help_in_group(message)
        else:
            msg = KurumiMessage.create(group_msg=message)
            for name, plugin_object in bot_core.plugin_objects.items():
                command_root = getattr(plugin_object, 'route', None)
                if command_root is not None and f"/{command_root}" in message.content:
                    command_params = message.content.split(command_root)[1].strip()
                    sub_command = command_params.split(" ")[0].strip()

                    command_found = False
                    for command_name, command_func in plugin_object.handlers.items():
                        if command_name == sub_command:
                            command_found = True
                            params = message.content.split(command_name)[1].strip()
                            await command_func["function"](plugin_object, message=msg, params=params)
                            return
                    if command_found is False and "main" in plugin_object.handlers:
                        await plugin_object.handlers["main"]["function"](plugin_object, message=msg,
                                                                         params=command_params)
                        return
            if "main" in bot_core.plugin_objects:
                main_object = bot_core.plugin_objects["main"]
                await main_object.handlers["main"]["function"](main_object,
                                                               message=msg,
                                                               params=message.content)

    async def on_at_message_create(self, message: Message):
        if bot_core.me["channel"] is None:
            bot_core.me["channel"] = await self.api.me()
        msg = KurumiMessage.create(channel_msg=message)

        bot_id = bot_core.me["channel"]["id"]
        if '/help' in message.content:
            await self.help(message)
        else:
            for name, plugin_object in bot_core.plugin_objects.items():
                command_root = getattr(plugin_object, 'route', None)
                if command_root is not None and f"<@!{bot_id}> /" + command_root in message.content:
                    command_params = message.content.split(command_root)[1].strip()
                    sub_command = command_params.split(" ")[0].strip()

                    command_found = False
                    for command_name, command_func in plugin_object.handlers.items():
                        if command_name == sub_command:
                            command_found = True
                            params = message.content.split(command_name)[1].strip()
                            await command_func["function"](plugin_object, message=msg, params=params)
                            return
                    if command_found is False and "main" in plugin_object.handlers:
                        await plugin_object.handlers["main"]["function"](plugin_object, message=msg,
                                                                         params=command_params)
                        return
            if "main" in bot_core.plugin_objects:
                command_params = message.content.split(f"<@!{bot_id}> ")[1].strip()
                main_object = bot_core.plugin_objects["main"]
                await main_object.handlers["main"]["function"](main_object,
                                                               message=msg,
                                                               params=command_params)
