from plugins.plugin import Plugin
from botpy.message import Message


class Manager(Plugin):
    name = "manager"

    def register_commands(self):
        @self.cmd("plugin", "插件功能")
        async def plugin(self, message: Message, params=None):
            # 第一种用reply发送消息
            #await message.reply(content=content)
            return True

