import disnake

from ...functions_handler import FunctionsHandler


class IsGuildExists(FunctionsHandler):
    def __init__(self, handler):
        super().__init__()
        self.handler = handler
        self.bot = handler.client.bot

    async def func_isguildexists(self, ctx: disnake.Message, args: str):
        """
        `$isGuildExists[guild]`
        """
        args_list = await self.get_args(await self.is_have_functions(args, ctx))
        if len(args_list) != 1:
            error_msg = "$isGuildExists: Too many or no args provided"
            if self.handler.debug_console:
                raise ValueError(error_msg)
            await ctx.channel.send(error_msg)
            return True

        if not args_list[0].isdigit():
            error_msg = f"$isGuildExists: Cannot find guild \"{args_list[0]}\""
            if self.handler.debug_console:
                raise SyntaxError(error_msg)
            await ctx.channel.send(error_msg)
            return True

        guild = self.bot.get_guild(int(args_list[0]))
        if not guild:
            guild = await self.bot.fetch_guild(int(args_list[0]))

        return "true" if guild else "false"

def setup(handler):
    return IsGuildExists(handler)