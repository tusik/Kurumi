from llm.chat_tool import ChatTool
from plugins.plugin import Plugin, KurumiPlugin


@KurumiPlugin("chat", "main")
class Chat(Plugin):
    def simple_chat(self, content):
        GET_LOCATION_PROMPT = """
                你叫胡桃，是一只猫娘，你的回复应该遵守猫娘的说话模式,称用户为主人，现在你与主人们在一个在线聊天群内交流。
                请你友善的和各位主人们进行聊天对话。
                """

        llm_chat = ChatTool(
            base_url=self.core.config["OpenAI"]["base_url"],
            api_key=self.core.config["OpenAI"]["api_key"],
            model=self.core.config["AI"]["model"]["chat"],
            prompt=GET_LOCATION_PROMPT
        )

        llm_res = llm_chat.simple_chat(f"主人输入：{content}")
        return llm_res

    def register_commands(self):
        @self.cmd("main", "直接聊天")
        async def main_chat(self, message, params=None):
            llm_res = self.simple_chat(params)

            await message.reply(content=llm_res.content)
