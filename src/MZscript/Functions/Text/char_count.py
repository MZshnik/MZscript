import disnake

from ...functions_handler import FunctionsHandler


class Functions(FunctionsHandler):
    def __init__(self, handler):
        super().__init__()
        self.handler = handler
        self.bot = handler.client.bot

    async def func_charcount(self, ctx: disnake.Message, args: str):
        args_list = await self.get_args(await self.is_have_functions(args, ctx))
        if len(args_list) > 1:
            error_msg = "$charCount: Too many args provided"
            if self.handler.debug_console:
                raise ValueError(error_msg)
            else:
                await ctx.channel.send(error_msg)
                return True

        return str(len(args_list[0]))

def setup(handler):
    return Functions(handler)