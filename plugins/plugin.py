import os

from bot.message import KurumiMessage, MessageType


def KurumiPlugin(name=None, route=None):
    def decorator(cls):
        print(f"注入新的插件: {cls.__name__}")
        cls.name = name if name else cls.__name__
        cls.route = route
        return cls

    return decorator


def get_bot_core():
    from bot.kurumi import bot_core
    return bot_core


class Plugin:
    def __init__(self, core, api=None, name=None, route=None):
        self.api = api
        if name is not None:
            self.name = name
        self.core = core
        if route is not None:
            self.route = route
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

    async def reply(self, msg: KurumiMessage):
        if msg.message_type == MessageType.Channel:

            await self.api.post_message(channel_id=msg.channel_id, msg_id=msg.message_id, content=msg.content,
                                        file_image=msg.file)
        elif msg.message_type == MessageType.Group:
            upload_media = None
            msg_type = 0
            if msg.file is not None:
                # 群只能从url读取图片
                filename = os.path.basename(msg.file)
                bot_core = get_bot_core()
                url = bot_core.config["group_url"]
                upload_media = await self.api.post_group_file(
                    group_openid=msg.group_id,
                    file_type=1,
                    url=f"{url}/{filename}"
                )
                msg_type = 7
            await self.api.post_group_message(group_openid=msg.group_id,
                                              msg_type=msg_type,
                                              msg_id=msg.message_id,
                                              content=msg.content,
                                              media=upload_media)
