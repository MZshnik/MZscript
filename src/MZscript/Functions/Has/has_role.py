import disnake

from ...functions_handler import FunctionsHandler


class Functions(FunctionsHandler):
    def __init__(self, handler):
        super().__init__()
        self.handler = handler
        self.bot = handler.client.bot

    async def func_hasrole(self, ctx: disnake.message.Message, args: str):
        """
        `$hasRole[(guild;user);role]`
        #### Example:
        `$hasRole[855478215266533426]`
        """
        args_list = await self.get_args(await self.is_have_functions(args, ctx))
        if len(args_list) == 0:
            raise ValueError(f"$hasRole: Needs 1 arguments, but only {len(args_list)} provided: \"{args}\"")

        guild = ctx.guild
        if args_list[0].isdigit() and len(args_list) > 1:
            try:
                guild = self.bot.get_guild(int(args_list[0]))
                if not guild:
                    guild = await self.bot.fetch_guild(int(args_list[0]))
                if not guild:
                    guild = ctx.guild
                    args_list.insert(0, guild)
            except Exception as e:
                print(e)
                raise SyntaxError(f"$hasRole: Cannot find guild \"{args_list[0]}\"")
        else:
            args_list.insert(0, guild)

        user = await guild.get_or_fetch_member(int(ctx.author.id))
        if args_list[1].isdigit() and len(args_list) > 2:
            try:
                user = await guild.get_or_fetch_member(int(args_list[1]))
                if not user:
                    raise SyntaxError(f"$hasRole: Cannot find user \"{args_list[1]}\"")
            except Exception as e:
                print(e)
                raise SyntaxError(f"$hasRole: Cannot find user \"{args_list[1]}\"")
        else:
            args_list.insert(1, user)

        role = None
        try:
            role = guild.get_role(int(args_list[2]))
            if not role:
                raise SyntaxError(f"$hasRole: Cannot find role \"{args_list[2]}\"")
        except Exception as e:
            print(e)
            raise SyntaxError(f"$hasRole: Cannot find role \"{args_list[2]}\"")

        if role in user.roles:
            return "true"
        return "false"

def setup(handler):
    return Functions(handler)
