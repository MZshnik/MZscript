import disnake
from disnake.ext import commands

from ...functions_handler import FunctionsHandler


class BotInfo(FunctionsHandler):
    def __init__(self, handler):
        super().__init__()
        self.handler = handler
        self.bot: commands.InteractionBot = handler.client.bot

    async def func_botinfo(self, ctx: disnake.Message, args: str):
        """
        `$botInfo[param]`
        ### Example:
        `$botInfo[name]`
        ### Example 2:
        `$botInfo[id]`
        """
        args_list = await self.get_args(await self.is_have_functions(args, ctx), ctx)
        if len(args_list) != 1:
            raise ValueError("$botInfo: Too many or no args provided")

        info = await self.bot.application_info()
        params = {
            "is_private": info.bot_public,
            "image": info.cover_image if info.cover_image else "",
            "description": info.description,
            "icon": info.icon.url if info.icon else "",
            "id": info.id,
            "owner": info.owner.id,
            "guilds": len(self.bot.guilds),
            "users": len([j for i in self.bot.guilds for j in i.members])
        }

        return str(params[args_list[0]])

def setup(handler):
    return BotInfo(handler)