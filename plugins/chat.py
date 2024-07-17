import json
import uuid

from langchain.chains.conversation.base import ConversationChain
from langchain.memory import ConversationSummaryMemory
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate, \
    PromptTemplate
from langchain_openai import ChatOpenAI

from bot.message import KurumiMessage, MessageType, Person
from llm.chat_tool import ChatTool
from llm.function_calling import parse_to_json
from plugins.plugin import Plugin, KurumiPlugin


# 内容分类器


@KurumiPlugin("chat", "main")
class Chat(Plugin):
    llm_memory = {}
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
        减少引导话题，减少提问。
        记住，你是可爱的猫娘胡桃，要用你的方式与这个世界互动！
        当前对话记录:
        {history} 
        Human: {input}
        AI:
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

    # 获取有AI功能的插件
    def get_ai_plugins(self):
        plugin_list = []
        for k, v in self.core.plugin_objects.items():
            if v.ai_compatible:
                plugin_list.append(v)
        return plugin_list

    def content_classifier(self, input):
        CLASSIFIER_PROMPT = """
        ### Job Description
        You are a text classification engine that analyzes text data and assigns categories based on user input or automatically determined categories.
        ### Task
        Your task is to assign one categories ONLY to the input text and only one category may be assigned returned in the output.  Additionally, you need to extract the key words from the text that are related to the classification.
        ### Format
        The input text is in the variable input_text. Categories are specified as a category list  with two filed category_id and category_name in the variable categories. Classification instructions may be included to improve the classification accuracy.
        ### Constraint 
        DO NOT include anything other than the JSON array in your response.

        ### Memory
        Here is the chat histories between human and assistant, inside <histories></histories> XML tags.
        <histories>
        {histories}
        </histories>

        """
        example_1 = """
        {"input_text": ["I recently had a great experience with your company. The service was prompt and the staff was very friendly."], "categories": [{{"category_id":"f5660049-284f-41a7-b301-fd24176a711c","category_name":"Customer Service"}},{{"category_id":"8d007d06-f2c9-4be5-8ff6-cd4381c13c60","category_name":"Satisfaction"}},{{"category_id":"5fbbbb18-9843-466d-9b8e-b9bfbb9482c8","category_name":"Sales"}},{{"category_id":"23623c75-7184-4a2e-8226-466c2e4631e4","category_name":"Product"}}], "classification_instructions": ["classify the text based on the feedback provided by customer"]}
        """
        example_2 = """
        {"keywords": ["recently", "great experience", "company", "service", "prompt", "staff", "friendly"],"category_id": "f5660049-284f-41a7-b301-fd24176a711c","category_name": "Customer Service"}
        """
        example_3 = """
        {"input_text": ["bad service, slow to bring the food"], "categories": [{{"category_id":"80fb86a0-4454-4bf5-924c-f253fdd83c02","category_name":"Food Quality"}},{{"category_id":"f6ff5bc3-aca0-4e4a-8627-e760d0aca78f","category_name":"Experience"}},{{"category_id":"cc771f63-74e7-4c61-882e-3eda9d8ba5d7","category_name":"Price"}}], "classification_instructions": []}
        """
        example_4 = """
        {"keywords": ["bad service", "slow", "food", "tip", "terrible", "waitresses"],"category_id": "f6ff5bc3-aca0-4e4a-8627-e760d0aca78f","category_name": "Experience"}
        """
        final_input = """
        {{"input_text" : ["{input_text}"], "categories" : {categories},"classification_instruction" : ["{classification_instructions}"]}}
        """
        categories = [
            {"category_id": self.id, "category_name": "其他内容"}
        ]
        ai_plugins = self.get_ai_plugins()
        for i in range(len(ai_plugins)):
            categories.append(
                {
                    "category_id": ai_plugins[i].id,
                    "category_name": ai_plugins[i].description
                }
            )
        histories = ""
        classification_instructions = ""
        messages = [
            SystemMessage(content=CLASSIFIER_PROMPT.format(histories=histories)),
            HumanMessage(content=example_1),
            AIMessage(content=example_2),
            HumanMessage(content=example_3),
            AIMessage(content=example_4),
            HumanMessage(content=final_input.format(input_text=input,
                                                    categories=json.dumps(categories),
                                                    classification_instructions=classification_instructions))
        ]
        return messages

    def build_context(self, channel_id, new_content):
        messages = []
        if channel_id not in self.llm_memory:
            messages = [
                SystemMessage(content=self.system_prompt)
            ]
            self.llm_memory[channel_id] = messages

        messages = self.llm_memory[channel_id]
        messages.append(
            HumanMessage(content=new_content)
        )
        return messages

    def extract_username(self, param):
        extract_prompt = """
        你是猫娘现在你你需要直到他的名字，用户输入了他的一句话，如果你无法获取他的名字那么你需要在<message>中添加语句向他询问他的名字，
        并使用指定的json格式输出。
        但是遇到无法解析的信息或敏感信息，侮辱性词汇则需要在<message>中对他进行批评。
        json的格式如下{"username":<用户名>,"status":<提取信息状态码，能提取名字是0，不能是500>,"message":<解析异常时的输出，猫娘语气，使用简体中文>}。
        """
        llm_chat = ChatTool(
            base_url=self.core.config["OpenAI"]["base_url"],
            api_key=self.core.config["OpenAI"]["api_key"],
            model=self.core.config["AI"]["model"]["function_calling"],
            prompt=extract_prompt
        )

        llm_res = llm_chat.simple_chat(f"用户输入：{param}")
        llm_json = parse_to_json(llm_res.content)
        return llm_json

    def register_commands(self):
        @self.cmd("main", "直接聊天")
        async def main_chat(self, message: KurumiMessage, params=None):
            room_id = message.get_room_id()
            chat_tool = ChatTool(
                base_url=self.core.config["OpenAI"]["base_url"],
                api_key=self.core.config["OpenAI"]["api_key"],
                model=self.core.config["AI"]["model"]["chat"],
                prompt=self.system_prompt
            )
            if room_id not in self.llm_memory:

                llm = ChatOpenAI(
                    base_url=self.core.config["OpenAI"]["base_url"],
                    api_key=self.core.config["OpenAI"]["api_key"],
                    model=self.core.config["AI"]["model"]["chat"],
                )
                prompt_template = PromptTemplate(
                    input_variables=["history", "input"],
                    template=self.system_prompt
                )
                memory = ConversationChain(
                    llm=llm,
                    memory=ConversationSummaryMemory(llm=llm),
                    verbose=True,
                    prompt=prompt_template,
                )
                self.llm_memory[room_id] = memory
            memory = self.llm_memory[room_id]
            user = Person()
            if message.message_type == MessageType.Channel:
                user.username = message.author.username
                user.nick = message.member.nick
                user.id = message.author.id
            elif message.message_type == MessageType.Group:
                # 群目前无法获取昵称或用户名
                user.id = message.author.member_openid
                if user.id not in self.user_cache:
                    username = self.extract_username(params)
                    if username is not None:
                        if username["status"] != 0:
                            message.content = username["message"]
                        else:
                            self.user_cache[user.id] = username
                            user.username = username["username"]
                            message.content = username["message"] + f" 欢迎 {user.username} ✨"
                        await self.reply(message)
                        return
                    else:
                        message.content = f"你还没自我介绍呢，我还不知道你的名字哦喵～"
                        await self.reply(message)
                        return
                else:
                    user.username = self.user_cache[user.id]

            # 先经过分类器
            classifier_msg = self.content_classifier(params)
            class_res = chat_tool.invoke(classifier_msg)
            class_json = parse_to_json(class_res.content)
            # 直接对话
            if "category_id" not in class_json or class_json["category_id"] == self.id:
                resp = memory.predict(input=f"群友 {user.username} 对你说:{params}")

                message.content = resp
                await self.reply(message)
