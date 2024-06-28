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
    handlers = {

    }
    api = None

    def __init__(self, name):
        self.name = name

    def run(self):
        print(f'Running plugin {self.name}')

    @classmethod
    def cmd(cls, alias: str):
        def decorator(func: Callable[[Any], Any]):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                return await func(*args, **kwargs)

            # 设置函数的别名
            wrapper.__alias__ = alias
            # 将函数添加到 handlers 字典中
            cls.handlers[alias] = wrapper
            return wrapper

        return decorator
