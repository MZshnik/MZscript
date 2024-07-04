import disnake

from ...functions_handler import FunctionsHandler


class Functions(FunctionsHandler):
    def __init__(self, handler):
        super().__init__()
        self.handler = handler
        self.bot = handler.client.bot

    async def func_addrole(self, ctx, args):
        """
        `$addRole[(guild;user);role]`
        """
        args_list = await self.get_args(await self.is_have_functions(args, ctx), ctx)
        if len(args_list) > 3 or len(args_list) == 0:
            error_msg = "$addRole: Too many or no args provided"
            if self.handler.debug_console:
                raise ValueError(error_msg)
            await ctx.channel.send(error_msg)
            return True

        guild = ctx.guild
        if len(args_list) == 3:
            if not args_list[0].isdigit():
                error_msg = f"$addRole: Cannot find guild \"{args_list[0]}\""
                if self.handler.debug_console:
                    raise SyntaxError(error_msg)
                await ctx.channel.send(error_msg)
                return True

            guild = self.bot.get_guild(int(args_list[0]))
            if not guild:
                guild = await self.bot.fetch_guild(int(args_list[0]))
        else:
            args_list.insert(0, guild)

        user = guild.get_member(ctx.author.id)
        if len(args_list) == 3:
            if not args_list[1].isdigit():
                error_msg = f"$addRole: Cannot find member \"{args_list[1]}\""
                if self.handler.debug_console:
                    raise SyntaxError(error_msg)
                await ctx.channel.send(error_msg)
                return True

            user = guild.get_member(int(args_list[1]))
            if not user:
                user = await guild.fetch_member(int(args_list[1]))
            if not user:
                error_msg = f"$addRole: Cannot find member \"{args_list[1]}\""
                if self.handler.debug_console:
                    raise SyntaxError(error_msg)
                await ctx.channel.send(error_msg)
                return True
        else:
            args_list.insert(0, user)

        role = guild.get_role(int(args_list[2]))
        if not role:
            error_msg = f"$addRole: Cannot find role \"{args_list[2]}\""
            if self.handler.debug_console:
                raise SyntaxError(error_msg)
            await ctx.channel.send(error_msg)
            return True

        reason = None
        if len(args_list) > 3:
            reason = args_list[3]

        await user.add_roles(role, reason=reason)

    async def func_removerole(self, ctx, args):
        """
        `$removeRole[(guild;user);role]`
        """
        args_list = await self.get_args(await self.is_have_functions(args, ctx), ctx)
        if len(args_list) > 3 or len(args_list) == 0:
            error_msg = "$removeRole: Too many or no args provided"
            if self.handler.debug_console:
                raise ValueError(error_msg)
            await ctx.channel.send(error_msg)
            return True

        guild = ctx.guild
        if len(args_list) == 3:
            if not args_list[0].isdigit():
                error_msg = f"$removeRole: Cannot find guild \"{args_list[0]}\""
                if self.handler.debug_console:
                    raise SyntaxError(error_msg)
                await ctx.channel.send(error_msg)
                return True

            guild = self.bot.get_guild(int(args_list[0]))
            if not guild:
                guild = await self.bot.fetch_guild(int(args_list[0]))
        else:
            args_list.insert(0, guild)

        user = guild.get_member(ctx.author.id)
        if len(args_list) == 3:
            if not args_list[1].isdigit():
                error_msg = f"$removeRole: Cannot find member \"{args_list[1]}\""
                if self.handler.debug_console:
                    raise SyntaxError(error_msg)
                await ctx.channel.send(error_msg)
                return True

            user = guild.get_member(int(args_list[1]))
            if not user:
                user = await guild.fetch_member(int(args_list[1]))
            if not user:
                error_msg = f"$removeRole: Cannot find member \"{args_list[1]}\""
                if self.handler.debug_console:
                    raise SyntaxError(error_msg)
                await ctx.channel.send(error_msg)
                return True
        else:
            args_list.insert(0, user)

        role = guild.get_role(int(args_list[2]))
        if not role:
            error_msg = f"$removeRole: Cannot find role \"{args_list[2]}\""
            if self.handler.debug_console:
                raise SyntaxError(error_msg)
            await ctx.channel.send(error_msg)
            return True

        reason = None
        if len(args_list) > 3:
            reason = args_list[3]

        await user.remove_roles(role, reason=reason)

def setup(handler):
    return Functions(handler)