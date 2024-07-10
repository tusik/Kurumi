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

    def build_context(self, prompt=None):
        system_msg = SystemMessage(content=self.prompt)
        if prompt is not None:
            system_msg = SystemMessage(content=prompt)
        return [system_msg] + self.messages

    def append(self, msg):
        self.messages.append(msg)

    def append_human(self, content):
        if isinstance(self.messages[-1], SystemMessage) or isinstance(self.messages[-1], AIMessage):
            self.messages.append(HumanMessage(content=content))
        else:
            raise ValueError("The last message must be a SystemMessage or AIMessage to append a HumanMessage.")

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

    def invoke(self, messages):
        llm = ChatOpenAI(
            base_url=self.base_url,
            api_key=self.api_key,
            model=self.model,
        )
        return llm.invoke(messages)

    def count_token(self):
        return count_token(self.messages)

    def summary(self, messages):
        prompt = "请总结以下对话的主要内容和结论，确保涵盖所有关键信息。"
