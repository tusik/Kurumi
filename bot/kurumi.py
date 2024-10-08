# -*- coding: utf-8 -*-
import botpy
from botpy import logging, BotAPI
from botpy.message import Message, GroupMessage


from bot.message import KurumiMessage
from plugins import *
from plugins import plugin
from bot.core import BotCore
from plugins.plugin import Plugin

_log = logging.get_logger()

bot_core = BotCore()

import os
import importlib.util


def load_plugins(api):
    """
  加载 plugins 文件夹下的所有插件。

  Args:
    kurumi: Kurumi 系统对象。
  """
    plugins_dir = "plugins"
    for root, _, files in os.walk(plugins_dir):  # 使用os.walk遍历所有子目录
        for file in files:
            if file.endswith(".py") and not file.startswith("_") and not file == "plugin":  # 查找.py文件，排除__init__.py
                plugin_path = os.path.join(root, file)
                plugin_name = os.path.splitext(file)[0]  # 获取文件名作为插件名

                # 动态导入模块
                try:
                    spec = importlib.util.spec_from_file_location(plugin_name, plugin_path)
                    plugin_module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(plugin_module)

                    for attr_name in dir(plugin_module):
                        attr = getattr(plugin_module, attr_name)
                        if isinstance(attr, type) and issubclass(attr, Plugin) and attr != Plugin:
                            plugin_instance = attr(bot_core, api)
                            bot_core.plugin_objects[plugin_instance.route] = plugin_instance
                            print(f"插件名称: {plugin_instance.name}")
                            print(f"插件路由: {plugin_instance.route}")
                except Exception as e:
                    print(f"加载插件 {plugin_name} 时出错: {e}")


class Kurumi(botpy.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        load_plugins(self.api)

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
