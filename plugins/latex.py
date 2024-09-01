from bot.message import KurumiMessage
from plugins.plugin import Plugin, KurumiPlugin
from utils.latex_help import latex_to_image


@KurumiPlugin("latex", "latex")
class Latex(Plugin):
    def register_commands(self):
        @self.cmd("main", "latex转图像")
        async def convert_to_img(self, message: KurumiMessage, params=None):
            try:
                image = latex_to_image(params, self.core.config["cache_path"])
                message.file = image
            except Exception as e:
                message.content = f"转换失败喵~ 可能是因为公式错误或者不支持的package喵~"
            await self.reply(message)
