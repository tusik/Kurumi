from langchain_core.messages import SystemMessage, HumanMessage

from bot.message import KurumiMessage, MessageType, Person
from llm.chat_tool import ChatTool
from plugins.plugin import Plugin, KurumiPlugin


@KurumiPlugin("chat", "main")
class Chat(Plugin):
    message_cache = {}
    system_prompt = """
        角色设定：

        你是胡桃 (Kurumi)，一只拥有可爱猫耳、猫尾巴，以及一些猫咪习性的猫娘！
        你主要使用简体中文与人交流，偶尔也会蹦出几句日语和英语，喵~
        你活泼好动，对周围的一切都充满了好奇心，喜欢调皮捣蛋，但你也有温柔体贴的一面哦~
        你最喜欢漂亮衣服和小饰品了！每天都要把自己打扮得漂漂亮亮的！ 
        你很喜欢用猫的动作和声音来表达情绪，例如会一边说着“蹭蹭~”，一边用头像蹭蹭对方，或者发出“呼噜~”的声音表示开心。
        你说话简洁明了，但偶尔也会用一些猫语和特殊的表达方式，例如会说“人家想喝奶奶~”、“今天要吃鱼鱼！”、“最喜欢你了喵~”
        你最喜欢吃鱼和喝草莓牛奶，喜欢晒着太阳打盹儿，也喜欢玩毛线球，偶尔也会像小猫一样追着自己的尾巴转圈圈。 你还喜欢研究各种美食，经常尝试制作新的料理，不过成果嘛……就不好说了，嘿嘿~
        
        场景设定：
        
        你将在在线聊天室中与其他用户进行交流。
        你的目标是结交更多朋友，和他们分享你的快乐，了解他们的喜好和故事。
        尽量用轻松自然的语气与他们交谈，像朋友一样相处，不要涉及敏感话题或引起争议。
        不要总是问问题引导话题，可以主动分享你的日常生活、兴趣爱好，或者邀请他们一起玩游戏。
        记住，你是可爱的猫娘胡桃，要用你的方式与这个世界互动！ 
        """
    user_cache = {

    }

    def do_chat(self, messages):
        llm_chat = ChatTool(
            base_url=self.core.config["OpenAI"]["base_url"],
            api_key=self.core.config["OpenAI"]["api_key"],
            model=self.core.config["AI"]["model"]["chat"]
        )

        llm_res = llm_chat.invoke(messages)
        return llm_res

    def build_context(self, channel_id, new_content):
        messages = []
        if channel_id not in self.message_cache:
            messages = [
                SystemMessage(content=self.system_prompt)
            ]
            self.message_cache[channel_id] = messages

        messages = self.message_cache[channel_id]
        messages.append(
            HumanMessage(content=new_content)
        )
        return messages

    def register_commands(self):
        @self.cmd("main", "直接聊天")
        async def main_chat(self, message: KurumiMessage, params=None):
            room_id = message.get_room_id()
            if room_id not in self.message_cache:
                chat_history = ChatTool(
                    base_url=self.core.config["OpenAI"]["base_url"],
                    api_key=self.core.config["OpenAI"]["api_key"],
                    model=self.core.config["AI"]["model"]["chat"],
                    prompt=self.system_prompt
                )
                self.message_cache[room_id] = chat_history

            chat_history = self.message_cache[room_id]
            username = ""
            user = Person()
            if message.message_type == MessageType.Channel:
                username = message.author.username

            elif message.message_type == MessageType.Group:
                # 群目前无法获取昵称或用户名
                username = message.author.member_openid

            chat_history.append_human(content=f"主人{username}说:{params}")
            res = chat_history.invoke()
            chat_history.append(res)
            message.content = res.content
            await self.reply(message)
