from plugins.plugin import Plugin, KurumiCommands
from botpy.message import Message

SYSTEM_PROMPT_COC = """
你将作为Call of Cthulhu跑团游戏的守密人，带领玩家们扮演的调查员进行游戏。
以下是现在的玩家,{player}
"""

GENERATE_PLAYER_PROMPT = """
请生成玩家的属性卡，属性卡包括以下属性：
力量（STR）、体质（CON）、体型（SIZ）、敏捷（DEX）、外貌（APP）、智力（INT）、意志（POW）、教育（EDU）
"""


class PlayerCard:
    _str = 0
    _con = 0
    _siz = 0
    _dex = 0
    _app = 0
    _int = 0
    _pow = 0
    _edu = 0


class COC(Plugin):
    prompt = ""
    name = "COC"

    @Plugin.cmd("coc")
    async def coc(self, message: Message, params=None):
        content = f"你好，{message.author.username}，你的参数是：dnd {params}"
        # 第一种用reply发送消息
        await message.reply(content=content)
        return True

    @Plugin.cmd("join")
    async def join(self, message: Message, params=None):
        content = f"你好，{message.author.username}，你的参数是：join {params}"
        # 第一种用reply发送消息
        await message.reply(content=content)
        return True
