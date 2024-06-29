import disnake

from ...functions_handler import FunctionsHandler


class isUserExists(FunctionsHandler):
    def __init__(self, handler):
        super().__init__()
        self.handler = handler
        self.bot = handler.client.bot

    async def func_isuserexists(self, ctx: disnake.Message, args: str):
        args_list = await self.get_args(await self.is_have_functions(args, ctx), ctx)
        
        if len(args_list) < 1 or len(args_list) == 0:
            raise ValueError("$isUserExists: To few or no args provided")

        
        if args_list[0].isdigit():
            user = self.bot.get_user(int(args_list[0]))
        else:
            raise SyntaxError(f"$isUserExists: User Id \"{args_list[0]}\", not integer")
        
        if user:
            return "true"
        else:
            return "false"

def setup(handler):
    return isUserExists(handler)