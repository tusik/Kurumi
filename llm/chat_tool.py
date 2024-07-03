from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage


class ChatTool:
    def __init__(self, prompt=None, base_url=None, api_key = None, model=None, user_content=None):
        self.prompt = prompt
        self.base_url = base_url
        self.api_key = api_key
        self.model = model
        self.user_content = user_content

    def simple_chat(self,content=None):
        llm = ChatOpenAI(
            base_url=self.base_url,
            api_key=self.api_key,
            model=self.model,
        )
        messages = [
            SystemMessage(content=self.prompt),
        ]
        if content is None:
            messages.append(HumanMessage(content=self.user_content))
        else:
            messages.append(HumanMessage(content=content))
        llm_resp = llm.invoke(messages)
        return llm_resp