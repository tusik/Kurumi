import time
import requests
from plugins.plugin import Plugin, KurumiPlugin
from llm.chat import Chat
from llm.function_calling import *
api_url = "https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={APIkey}"

@KurumiPlugin(name="Weather")
class Weather(Plugin):
    def get_location_llm(self, content):
        GET_LOCATION_PROMPT = """
        你是文本提取工具，你能提取以下内容中的地址，并输出经纬度到以下json格式中:
        {\"lat\":地址的纬度,\"lon\":地址的经度,\"location\":地址的英文名称}.
        最后只输出json内容给用户
        """

        llm_chat = Chat(
            base_url=self.core.config["OpenAI"]["base_url"], 
            api_key=self.core.config["OpenAI"]["api_key"],
            model="llama3-8b-8192",
            prompt=GET_LOCATION_PROMPT
            )
        
        llm_res =llm_chat.simple_chat(content)
        llm_json = parse_to_json(llm_res.content)
        return llm_json
            
    def register_commands(self):
        @self.cmd("/weather", "获取天气信息")
        async def weather(self, message, params=None):
            if params == None:
                await message.reply(content="你还没告诉我哪里喵~")
                return False
            llm_json = self.get_location_llm(params)
            if llm_json == None:
                await message.reply(content="解析地址失败喵~")
                return False
            url = api_url.format(lat=llm_json["lat"], lon=llm_json["lon"], APIkey=self.core.config["OpenWeather"]["api_key"])

            response = requests.get(url)
            await message.reply(content=response.text)
            return True

        