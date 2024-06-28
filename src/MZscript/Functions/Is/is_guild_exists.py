import disnake

from functions_handler import FunctionsHandler


class isGuildExists(FunctionsHandler):
    def __init__(self, handler):
        super().__init__()
        self.handler = handler
        self.bot = handler.client.bot

    async def func_isguildexists(self, ctx: disnake.message.Message, args: str):
        args_list = await self.get_args(await self.is_have_functions(args, ctx), ctx)
        
        if len(args_list) < 1 or len(args_list) == 0:
            raise ValueError("$isGuildExists: To few or no args provided")

        
        if args_list[0].isdigit():
            user = self.bot.get_guild(int(args_list[0]))
        else:
            raise SyntaxError(f"$isGuildExists: Guild Id \"{args_list[0]}\", not integer")
        
        if user:
            return "true"
        else:
            return "false"

def setup(handler):
    return isGuildExists(handler)