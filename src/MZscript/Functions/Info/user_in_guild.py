import disnake

from ...functions_handler import FunctionsHandler


class UserInGuild(FunctionsHandler):
    def __init__(self, handler):
        super().__init__()
        self.handler = handler
        self.bot = handler.client.bot

    async def func_useringuild(self, ctx: disnake.message.Message, args: str):
        args_list = await self.get_args(await self.is_have_functions(args, ctx), ctx)
        
        if len(args_list) < 1 or len(args_list) == 0:
            raise ValueError("$userInGuild: To few or no args provided")
        if not args_list[0].isdigit():
            raise SyntaxError(f"$userInGuild: User id: \"{args_list[0]}\", not int")
        if len(args_list) >= 2:
            if not args_list[1].isdigit():
                raise SyntaxError(f"$userInGuild: Guild id: \"{args_list[1]}\", not int")
            guild = self.bot.get_guild(int(await self.is_have_functions(args_list[1], ctx)))
            if not guild:
                raise SyntaxError(f"$userInGuild: Cannot find guild \"{await self.is_have_functions(args_list[1], ctx)}\"")
        else:
            guild = self.bot.get_guild(ctx.guild.id)
        
        user = guild.get_member(int(await self.is_have_functions(args_list[0], ctx)))
        
        if user:
            return "true"
        else:
            return "false"

def setup(handler):
    return UserInGuild(handler)