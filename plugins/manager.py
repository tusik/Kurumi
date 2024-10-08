from bot.message import KurumiMessage, MessageType
from plugins.plugin import Plugin, KurumiPlugin
from botpy.message import Message


@KurumiPlugin(name="manager", route="系统")
class Manager(Plugin):

    def register_commands(self):
        @self.cmd("main", "插件功能")
        async def plugin(self, message: KurumiMessage, params=None):
            if params == "help":
                content = "以下是plugin命令可用的参数：\n"
                content = content + "/plugin list: 列出所有插件\n"
                content = content + "/plugin reload [name]: 重载插件\n"
                message.content = content
            elif "reload" in params:
                texts = params.split(" ")
                if len(texts) < 2:
                    message.content = "缺少参数: name"
                    await self.reply(message)
                    return False
                plugin_name = texts[1]
                if plugin_name in self.core.plugin_objects:
                    self.core.plugin_objects[plugin_name] = self.core.plugin_objects[plugin_name].__class__(self.core,
                                                                                                            api=self.api)
                    message.content = f"插件[{plugin_name}]重载成功喵~"
                else:
                    message.content = f"插件[{plugin_name}]不存在"
            elif "list" in params:
                content = "以下是现在支持的插件：\n"
                for name, plugin_object in self.core.plugin_objects.items():
                    content = content + f"插件名 {name}\n"
                message.content = content

            await self.reply(message)
            return True

        @self.cmd("me", "获取用户当前信息")
        async def me(self, message: KurumiMessage, params=None):
            if message.message_type == MessageType.Channel:
                roles = []
                for i in message.member.roles:
                    if i == '2':
                        roles.append("管理员")
                    elif i == '4':
                        roles.append("群主")
                    elif i == '5':
                        roles.append("子频道管理员")
                content = f"用户[{message.member.nick}-{message.author.id}]-{roles}\n"
                message.content = content
            else:
                message.content = "QQ群不支持此功能啊喵～"

            await self.reply(message)
            return True
