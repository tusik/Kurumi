from botpy.message import Message

from plugins.plugin import Plugin, KurumiPlugin

@KurumiPlugin(name="DND")
class DND(Plugin):
    def register_commands(self):
        @self.cmd("/dnd", "这是一个DND游戏的插件")
        async def dnd(self, message, params=None):
            content = f"你好，{message.author.username}，你的参数是：dnd {params}"
            await message.reply(content=content)
            return True

        @self.cmd("/join", "加入游戏")
        async def join(self, message, params=None):
            content = f"你好，{message.author.username}，你的参数是：join {params}"
            await message.reply(content=content)
            return True
