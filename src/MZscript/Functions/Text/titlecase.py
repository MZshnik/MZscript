import disnake

from functions_handler import FunctionsHandler


class Functions(FunctionsHandler):
    def __init__(self, handler):
        super().__init__()
        self.handler = handler
        self.bot = handler.client.bot

    # [text]
    async def func_titlecase(self, ctx: disnake.message.Message, args: str):
        args_list = await self.get_args(await self.is_have_functions(args, ctx))
        
        return args_list[0].title()
        
def setup(handler):
    return Functions(handler)