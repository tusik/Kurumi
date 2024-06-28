import os
from functools import wraps
from typing import List, Callable, Any
from botpy import logging, BotAPI

from botpy.ext.command_util import Commands
from botpy.message import BaseMessage

from plugins import *


def KurumiPlugin(cls):
    print(f"注册新的插件: {cls.__name__}")

    def decorator():
        plugin_list.append(cls())
        return cls

    return decorator


class KurumiCommands:
    """
    指令装饰器

    Args:
      args (tuple): 字符串元组。
    """

    def __init__(self, *args):
        self.commands = args

    def __call__(self, func):
        @wraps(func)
        async def decorated(*args, **kwargs):
            print(args, kwargs)
            message: BaseMessage = args[2]
            for command in self.commands:
                if command in message.content:
                    # 分割指令后面的指令参数
                    params = message.content.split(command)[1].strip()
                    kwargs["params"] = params
                    return await func(*args, **kwargs)
            return False

        return decorated


class Plugin:
    def __init__(self, api=None, name=None):
        self.api = api
        self.name = name
        self.handlers = {}
        self.register_commands()

    def register_commands(self):
        pass

    def run(self):
        print(f'Running plugin {self.name}')

    def cmd(self, alias, description):
        def decorator(func):
            self.handlers[alias] = {
                'function': func,
                'description': description
            }
            return func

        return decorator

    def get_cmd_describe(self):
        content = ""
        for alias, handler in self.handlers.items():
            desc = handler["description"]
            content = content + f"{alias}: {desc} \n"
        return content
