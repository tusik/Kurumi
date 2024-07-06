# -*- coding: utf-8 -*-
import os
import botpy
from botpy.ext.cog_yaml import read
from bot import kurumi
script_path = os.path.abspath(__file__)
# 获取当前脚本所在的目录
script_dir = os.path.dirname(script_path)
config = read(os.path.join(script_dir, "config.yaml"))

if __name__ == '__main__':
    intents = botpy.Intents(public_guild_messages=True,public_messages=True)
    client = kurumi.Kurumi(intents=intents)
    client.set_config(config)
    client.run(appid=config["appid"], secret=config["secret"])