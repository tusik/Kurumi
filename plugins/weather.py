import time
import requests
from plugins.plugin import Plugin, KurumiPlugin
from llm.chat import Chat
from llm.function_calling import *
from botpy.types.message import Embed, EmbedField
from utils.weather_help import draw_today

api_url = "https://api.openweathermap.org/data/2.5/weather?q={city},{country}&appid={APIkey}"


def f_to_c(f):
    return round((f - 32.0) / 1.8, 1)


def k_to_c(k):
    return round(k - 273.15, 1)


@KurumiPlugin(name="Weather")
class Weather(Plugin):
    def get_location_llm(self, content):
        GET_LOCATION_PROMPT = """
        你是文本提取工具，你能提取以下内容中的地址，并输出经纬度到以下json格式中:
        {\"city name\":城市英文名,\"state code\":州代码,\"country code\":国家代码}
        最后只输出json内容给用户
        """

        llm_chat = Chat(
            base_url=self.core.config["OpenAI"]["base_url"],
            api_key=self.core.config["OpenAI"]["api_key"],
            model="llama3-8b-8192",
            prompt=GET_LOCATION_PROMPT
        )

        llm_res = llm_chat.simple_chat(content)
        llm_json = parse_to_json(llm_res.content)
        return llm_json

    def register_commands(self):
        @self.cmd("/weather", "获取天气信息")
        async def weather(self, message, params=None):
            plugin_config = self.core.config["plugins"]["weather"]
            if params is None:
                await message.reply(content="你还没告诉我哪里喵~")
                return False
            llm_json = self.get_location_llm(params)
            if llm_json is None:
                await message.reply(content="解析地址失败喵~")
                return False
            url = api_url.format(city=llm_json["city name"], country=llm_json["country code"],
                                 APIkey=plugin_config["OpenWeather"]["api_key"])

            response = requests.get(url)
            image = draw_today(response.text, plugin_config["cache_path"])
            if image is None:
                await self.api.post_message(channel_id=message.channel_id, msg_id=message.id, content="绘制图形失败喵~")
            else:
                await self.api.post_message(channel_id=message.channel_id, msg_id=message.id, file_image=image)
            return True
