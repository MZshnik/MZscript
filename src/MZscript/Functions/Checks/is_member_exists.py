import disnake

from ...functions_handler import FunctionsHandler


class isMemberExists(FunctionsHandler):
    def __init__(self, handler):
        super().__init__()
        self.handler = handler
        self.bot = handler.client.bot

    async def func_ismemberexists(self, ctx: disnake.Message, args: str):
        """
        `$isMemberExists[(guild);user]`
        """
        args_list = await self.get_args(await self.is_have_functions(args, ctx), ctx)
        if len(args_list) > 2 or len(args_list) == 0:
            raise ValueError("$isMemberExists: Too many or no args provided")

        guild = ctx.guild
        if len(args_list) == 2:
            if not args_list[0].isdigit():
                error_msg = f"$isMemberExists: Cannot find guild \"{args_list[0]}\""
                if self.handler.debug_console:
                    raise SyntaxError(error_msg)
                await ctx.channel.send(error_msg)
                return True

            guild = self.bot.get_guild(int(args_list[0]))
            if not guild:
                guild = await self.bot.fetch_guild(int(args_list[0]))
            if not guild:
                error_msg = f"$isMemberExists: Cannot find guild \"{args_list[0]}\""
                if self.handler.debug_console:
                    raise SyntaxError(error_msg)
                await ctx.channel.send(error_msg)
                return True
        else:
            args_list.insert(0, guild)

        user = await guild.get_or_fetch_member(int(ctx.author.id))
        if len(args_list) > 1:
            if not args_list[0].isdigit():
                error_msg = f"$isMemberExists: Cannot find user \"{args_list[1]}\""
                if self.handler.debug_console:
                    raise SyntaxError(error_msg)
                await ctx.channel.send(error_msg)
                return True

            user = await guild.get_or_fetch_member(int(args_list[1]))

        return "true" if user else "false"

def setup(handler):
    return isMemberExists(handler)