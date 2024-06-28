import disnake

from ...functions_handler import FunctionsHandler


class Functions(FunctionsHandler):
    def __init__(self, handler):
        super().__init__()
        self.handler = handler
        self.bot = handler.client.bot

    # [text]
    async def func_isnumber(self, ctx: disnake.message.Message, args: str):
        args_list = await self.get_args(await self.is_have_functions(args, ctx))

        if len(args_list) > 0:
            if args_list[0].isdigit():
                to_return = "true"
            try:
                float(args_list[0])
                to_return = "true"
            except:
                to_return = "false"
        else:
            to_return = "false"
        
        return to_return
        
def setup(handler):
    return Functions(handler)