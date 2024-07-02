from plugins.plugin import Plugin, KurumiPlugin
from utils.latex_help import latex_to_image


@KurumiPlugin("latex", "latex")
class Latex(Plugin):
    def register_commands(self):
        @self.cmd("main", "latex转图像")
        async def convert_to_img(self, message, params=None):
            image = latex_to_image(params, self.core.config["cache_path"])
            await self.api.post_message(channel_id=message.channel_id, msg_id=message.id, file_image=image)
