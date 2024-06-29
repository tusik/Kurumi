# -*- coding: utf-8 -*-
import os
import botpy
from botpy.ext.cog_yaml import read
from bot import kurumi
config = read(os.path.join(os.path.dirname(__file__), "config.yaml"))

if __name__ == '__main__':
    intents = botpy.Intents(public_guild_messages=True) 
    client = kurumi.Kurumi(intents=intents)
    client.set_config(config)
    client.run(appid=config["appid"], secret=config["secret"])