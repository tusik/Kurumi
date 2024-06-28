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

        @self.cmd("me", "获取用户当前信息")
        async def plugin(self, message: Message, params=None):
            roles = []
            for i in message.member.roles:
                if i == '2':
                    roles.append("管理员")
                elif i == '4':
                    roles.append("群主")
                elif i == '5':
                    roles.append("子频道管理员")
            content = f"用户[{message.member.nick}-{message.author.id}]-{roles}\n"
            await message.reply(content=content)
            return True