import disnake

from ...functions_handler import FunctionsHandler


class isUserExists(FunctionsHandler):
    def __init__(self, handler):
        super().__init__()
        self.handler = handler
        self.bot = handler.client.bot

    async def func_isuserexists(self, ctx: disnake.Message, args: str):
        """
        `$isUserExists[user]`
        """
        args_list = await self.get_args(await self.is_have_functions(args, ctx), ctx)
        if len(args_list) != 1:
            error_msg = "$isUserExists: Too many or no args provided"
            if self.handler.debug_console:
                raise SyntaxError(error_msg)
            await ctx.channel.send(error_msg)
            return True

        if not args_list[0].isdigit():
            error_msg = f"$isUserExists: Cannot find user \"{args_list[0]}\""
            if self.handler.debug_console:
                raise SyntaxError(error_msg)
            await ctx.channel.send(error_msg)
            return True

        return "true" if await self.bot.get_or_fetch_user(int(args_list[0])) else "false"

def setup(handler):
    return isUserExists(handler)