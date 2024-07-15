import disnake

from ...functions_handler import FunctionsHandler


class IsNumber(FunctionsHandler):
    def __init__(self, handler):
        super().__init__()
        self.handler = handler
        self.bot = handler.client.bot

    async def func_isnumber(self, ctx: disnake.Message, args: str):
        """
        `$isNumber[text]`
        """
        args_list = await self.get_args(await self.is_have_functions(args, ctx))
        if len(args_list) != 1:
            error_msg = "$isNumber: Too many args provided"
            if self.handler.debug_console:
                raise ValueError(error_msg)
            await ctx.channel.send(error_msg)
            return True

        if len(args_list) != 0:
            try:
                float(args_list[0])
                return "true"
            except:
                return "false"
        return "false"

def setup(handler):
    return IsNumber(handler)