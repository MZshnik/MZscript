import disnake

from ...functions_handler import FunctionsHandler


class isRoleExists(FunctionsHandler):
    def __init__(self, handler):
        super().__init__()
        self.handler = handler
        self.bot = handler.client.bot

    async def func_isroleexists(self, ctx: disnake.Message, args: str):
        """
        `$isRoleExists[(guild);role]`
        """
        args_list = await self.get_args(await self.is_have_functions(args, ctx), ctx)
        if len(args_list) > 2 or len(args_list) == 0:
            error_msg = "$isRoleExists: Too many or no args provided"
            if self.handler.debug_console:
                raise ValueError(error_msg)
            await ctx.channel.send(error_msg)
            return True

        guild = ctx.guild
        if len(args_list) > 1:
            if not args_list[0].isdigit():
                error_msg = f"$isRoleExists: Cannot find guild \"{args_list[0]}\""
                if self.handler.debug_console:
                    raise SyntaxError(error_msg)
                await ctx.channel.send(error_msg)
                return True
            guild = self.bot.get_guild(int(args_list[0]))
            if not guild:
                guild = await self.bot.fetch_guild(int(args_list[0]))
            if not guild:
                error_msg = f"$isRoleExists: Cannot find guild \"{args_list[0]}\""
                if self.handler.debug_console:
                    raise SyntaxError(error_msg)
                await ctx.channel.send(error_msg)
                return True
        else:
            args_list.insert(1, guild)

        if not args_list[1].isdigit():
            error_msg = f"$isRoleExists: Role id most be integer \"{args_list[1]}\""
            if self.handler.debug_console:
                raise SyntaxError(error_msg)
            await ctx.channel.send(error_msg)
            return True

        return "true" if guild.get_role(int(args_list[1])) else "false"

def setup(handler):
    return isRoleExists(handler)