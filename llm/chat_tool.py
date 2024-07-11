from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
import tiktoken

encoding = tiktoken.get_encoding("cl100k_base")


def count_token(messages):
    count = 0
    for msg in messages:
        tokens = encoding.encode(msg.content)
        count = count + len(tokens)


class ChatTool:
    def __init__(self, prompt=None, base_url=None, api_key=None, model=None):
        self.prompt = prompt if prompt is not None else "You are a helpful assistant."
        self.base_url = base_url
        self.api_key = api_key
        self.model = model
        self.messages = []
        self.summary_context = None

    def build_context(self, prompt=""):
        msg_list = []
        temp_prompt = ""
        if prompt != "":
            temp_prompt = prompt
        else:
            temp_prompt = self.prompt
        if self.summary_context is not None:
            temp_prompt = (temp_prompt +
                           f"。以下内容是用户与你之前对话的总结内容\n**历史对话总结**{self.summary_context}**历史对话总结结束**")

        msg_list.append(SystemMessage(content=temp_prompt))
        msg_list.extend(self.messages)
        return msg_list

    def append(self, msg):
        self.messages.append(msg)

    def append_human(self, content):
        self.messages.append(HumanMessage(content=content))

    def append_assistant(self, content):
        if isinstance(self.messages[-1], HumanMessage):
            self.messages.append(HumanMessage(content=content))
        else:
            raise ValueError("The last message must be a SystemMessage or AIMessage to append a HumanMessage.")

    def simple_chat(self, content=None):
        llm = ChatOpenAI(
            base_url=self.base_url,
            api_key=self.api_key,
            model=self.model,
        )
        if content is not None:
            self.append_human(content)
        llm_resp = llm.invoke(self.build_context())
        return llm_resp

    def invoke(self, messages=None):
        llm = ChatOpenAI(
            base_url=self.base_url,
            api_key=self.api_key,
            model=self.model,
        )
        if messages is None:
            return llm.invoke(self.build_context())
        else:
            return llm.invoke(messages)

    def count_token(self):
        return count_token(self.messages)

    def summary(self, messages):
        message_list = messages
        if messages is None:
            prompt = "请总结以下对话的主要内容和结论，确保涵盖所有关键信息。"
            message_list = self.build_context(prompt)
        message_list.append(
            HumanMessage(content="总结以上内容。")
        )
        res = self.invoke(message_list)
        self.messages = []
        self.summary_context = res.content

