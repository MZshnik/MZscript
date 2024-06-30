import disnake

from ...functions_handler import FunctionsHandler


class Functions(FunctionsHandler):
    def __init__(self, handler):
        super().__init__()
        self.handler = handler
        self.bot = handler.client.bot

    async def func_hasrole(self, ctx: disnake.Message, args: str):
        """
        `$hasRole[(guild;user);role]`
        #### Example:
        `$hasRole[855478215266533426]`
        """
        args_list = await self.get_args(await self.is_have_functions(args, ctx))
        if len(args_list) == 0:
            error_msg = f"$hasRole: Too many or no args provided"
            if self.handler.debug_console:
                raise ValueError(error_msg)
            await ctx.channel.send(error_msg)
            return True

        guild = ctx.guild
        if args_list[0].isdigit() and len(args_list) > 1:
            guild = self.bot.get_guild(int(args_list[0]))
            if not guild:
                guild = await self.bot.fetch_guild(int(args_list[0]))
            if not guild:
                guild = ctx.guild
                args_list.insert(0, guild)
        else:
            args_list.insert(0, guild)

        user = await guild.get_or_fetch_member(int(ctx.author.id))
        if args_list[1].isdigit() and len(args_list) > 2:
            user = await guild.get_or_fetch_member(int(args_list[1]))
            if not user:
                if self.handler.debug_console:
                    raise SyntaxError(f"$hasRole: Cannot find user \"{args_list[1]}\"")
                await ctx.channel.send(error_msg)
                return True
        else:
            args_list.insert(1, user)

        role = None
        if args_list[2].isdigit():
            role = guild.get_role(int(args_list[2]))
            if not role:
                if self.handler.debug_console:
                    raise SyntaxError(f"$hasRole: Cannot find role \"{args_list[2]}\"")
                await ctx.channel.send(error_msg)
                return True
        else:
            if self.handler.debug_console:
                raise SyntaxError(f"$hasRole: Cannot find role \"{args_list[2]}\"")
            await ctx.channel.send(error_msg)
            return True

        return "true" if role in user.roles else "false"

def setup(handler):
    return Functions(handler)
