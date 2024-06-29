import disnake

from ...functions_handler import FunctionsHandler


class Functions(FunctionsHandler):
    def __init__(self, handler):
        super().__init__()
        self.handler = handler
        self.bot = handler.client.bot

    async def func_titlecase(self, ctx: disnake.message.Message, args: str):
        args_list = await self.get_args(await self.is_have_functions(args, ctx))
        if len(args_list) > 1 or len(args_list) == 0:
            error_msg = "$upperCase: Too many or no args provided"
            if self.handler.debug_console:
                raise ValueError(error_msg)
            else:
                await ctx.channel.send(error_msg)
                return True

        return args_list[0].title()
        
def setup(handler):
    return Functions(handler)