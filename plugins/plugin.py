import os
from functools import wraps
from typing import List, Callable, Any
from botpy import logging, BotAPI

from botpy.ext.command_util import Commands
from botpy.message import BaseMessage

from plugins import *

def KurumiPlugin(name=None):
    def decorator(cls):
        print(f"注册新的插件: {cls.__name__}")
        cls.name = name if name else cls.__name__
        return cls
    return decorator


class Plugin:
    def __init__(self, core, api=None, name=None):
        self.api = api
        if name is not None:
            self.name = name
        self.core = core
        self.handlers = {}
        self.register_commands()

    def __del__(self):
        print(f"卸载插件: {self.name}")

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
