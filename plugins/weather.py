import os
import time
import requests

from bot.message import KurumiMessage
from plugins.plugin import Plugin, KurumiPlugin
from llm.chat_tool import ChatTool
from llm.function_calling import *
from botpy.types.message import Embed, EmbedField
from utils.weather_help import draw_today

api_url = "https://api.openweathermap.org/data/2.5/weather?q={city},{country}&appid={APIkey}&lang=zh_cn"


def f_to_c(f):
    return round((f - 32.0) / 1.8, 1)


def k_to_c(k):
    return round(k - 273.15, 1)


@KurumiPlugin(name="Weather", route="天气", description="查询天气相关信息", ai_compatible=True)
class Weather(Plugin):
    def get_location_llm(self, content):
        GET_LOCATION_PROMPT = """
        你叫胡桃，是一只猫娘，你的回复应该遵守猫娘的说话模式,称用户为主人，现在你能从用户给出的文本中提取以下内容中的地址，并输出信息到以下json格式中json:
        {\"city name\":<城市英文名>,\"state code\":<州代码，可以为空>,
        \"country code\":<国家代码>,\"error_message\":<无法解析时添加的中文错误信息，遵守猫娘说话模式>}。
        你有且只能输出中文的json格式的内容
        """

        llm_chat = ChatTool(
            base_url=self.core.config["OpenAI"]["base_url"],
            api_key=self.core.config["OpenAI"]["api_key"],
            model=self.core.config["AI"]["model"]["function_calling"],
            prompt=GET_LOCATION_PROMPT
        )

        llm_res = llm_chat.simple_chat(f"用户输入：{content}")
        llm_json = parse_to_json(llm_res.content)
        return llm_json

    def register_commands(self):
        @self.cmd("main", "获取天气信息")
        async def weather(self, message: KurumiMessage, params=None):
            plugin_config = self.core.config["plugins"]["weather"]
            if params is None:
                message.content = "你还没告诉我哪里喵~"
                await self.reply(message)
                return False
            llm_json = self.get_location_llm(params)
            if llm_json is None:
                message.content = "解析地址失败喵~"
                await self.reply(message)
                return False
            if llm_json["city name"] == "" and llm_json["country code"] == "" and llm_json["error_message"] != "":
                message.content = llm_json["error_message"]
                await self.reply(message)
                return False
            url = api_url.format(city=llm_json["city name"], country=llm_json["country code"],
                                 APIkey=plugin_config["OpenWeather"]["api_key"])

            response = requests.get(url)
            image = draw_today(response.text, self.core.config["cache_path"])
            if image is None:
                message.content = "绘制图形失败喵~"
                await self.reply(message)
            else:
                message.set_image(os.path.abspath(image))
                await self.reply(message)
            return True
