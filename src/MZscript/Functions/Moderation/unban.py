import disnake

from ...functions_handler import FunctionsHandler


class FuncUnban(FunctionsHandler):
    def __init__(self, handler):
        super().__init__()
        self.handler = handler
        self.bot = handler.client.bot

    async def func_unban(self, ctx: disnake.Message, args: str = None):
        """
        `$unban[(guild);user;(reason)]`
        """
        args_list = await self.get_args(await self.is_have_functions(args, ctx))
        if len(args_list) > 3 or len(args_list) == 0:
            error_msg = "$unban: Too many or no args provided"
            if self.handler.debug_console:
                raise ValueError(error_msg)
            else:
                await ctx.channel.send(error_msg)
                return True

        guild = ctx.guild
        if len(args_list) > 1:
            try:
                guild = self.bot.get_guild(int(args_list[0]))
                if not guild:
                    guild = await self.bot.fetch_guild(int(args_list[0]))
                if not guild:
                    guild = ctx.guild
                    args_list.insert(0, guild)
            except Exception as e:
                print(e)
                raise SyntaxError(f"$unban: Cannot find guild \"{args_list[0]}\"")
        else:
            args_list.insert(0, guild)

        user = await self.bot.get_or_fetch_user(args_list[1])

        reason = None
        if len(args_list) > 2:
            reason = args_list[2]

        await guild.unban(user=user, reason=reason)

def setup(handler):
    return FuncUnban(handler)