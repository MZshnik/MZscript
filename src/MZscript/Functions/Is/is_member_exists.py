import disnake

from functions_handler import FunctionsHandler


class isMemberExists(FunctionsHandler):
    def __init__(self, handler):
        super().__init__()
        self.handler = handler
        self.bot = handler.client.bot

    async def func_ismemberexists(self, ctx: disnake.message.Message, args: str):
        args_list = await self.get_args(await self.is_have_functions(args, ctx), ctx)
        
        if len(args_list) < 1 or len(args_list) == 0:
            raise ValueError("$isMemberExists: To few or no args provided")
        guild = ctx.guild
        if len(args_list) > 1:
            if args_list[1].isdigit():
                try:
                    guild = self.bot.get_guild(int(args_list[1]))
                    if not guild:
                        guild = await self.bot.fetch_guild(int(args_list[1]))
                    if not guild:
                        guild = ctx.guild
                        args_list.insert(1, guild)
                except Exception as e:
                    print(e)
                    raise SyntaxError(f"$userInGuild: Cannot find guild \"{args_list[1]}\"")
            else:
                raise SyntaxError(f"$userInGuild: Cannot find guild \"{args_list[1]}\"")
        else:
            args_list.insert(1, guild)

        
        if args_list[0].isdigit():
                user = await guild.get_or_fetch_member(int(args_list[0]))
        else:
            raise SyntaxError(f"$userInGuild: User Id \"{args_list[0]}\", not integer")
        
        if user:
            return "true"
        else:
            return "false"

def setup(handler):
    return isMemberExists(handler)