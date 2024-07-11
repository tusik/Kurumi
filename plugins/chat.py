from langchain_core.messages import SystemMessage, HumanMessage

from bot.message import KurumiMessage, MessageType
from llm.chat_tool import ChatTool
from plugins.plugin import Plugin, KurumiPlugin


@KurumiPlugin("chat", "main")
class Chat(Plugin):
    message_cache = {}
    system_prompt = """
                    你叫胡桃，是一只猫娘，你的回复应该遵守猫娘的说话模式,称用户为主人，现在你与主人们在一个在线聊天群内交流。
                    请你友善的和各位主人们进行聊天对话。
                    """

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
            if message.message_type == MessageType.Channel:
                user_name = message.author.username
                messages = self.build_context(message.channel_id, f"主人{user_name}说:{params}")
                llm_res = self.do_chat(messages)
                messages.append(llm_res)
                message.content = llm_res.content
                await self.reply(message)
            elif message.message_type == MessageType.Group:
                if message.group_id not in self.message_cache:
                    chat_history = ChatTool(
                        base_url=self.core.config["OpenAI"]["base_url"],
                        api_key=self.core.config["OpenAI"]["api_key"],
                        model=self.core.config["AI"]["model"]["chat"],
                        prompt=self.system_prompt
                    )
                    self.message_cache[message.group_id] = chat_history
                chat_history = self.message_cache[message.group_id]
                user_id = message.author.member_openid
                chat_history.append_human(content=f"主人{user_id}说:{params}")
                res = chat_history.invoke()
                chat_history.append(res)
                message.content = res.content
                await self.reply(message)
