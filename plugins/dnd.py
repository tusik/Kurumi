from plugins.plugin import Plugin, KurumiCommands
from botpy.message import Message


class DND(Plugin):
    def __init__(self, api):
        super().__init__("DND")
        self.api = api

    @Plugin.cmd("dnd")
    async def dnd(self, message: Message, params=None):
        content = f"你好，{message.author.username}，你的参数是：dnd {params}"
        # 第一种用reply发送消息
        await message.reply(content=content)
        return True

    @Plugin.cmd("join")
    async def join(self, message: Message, params=None):
        content = f"你好，{message.author.username}，你的参数是：join {params}"
        # 第一种用reply发送消息
        await message.reply(content=content)
        return True
