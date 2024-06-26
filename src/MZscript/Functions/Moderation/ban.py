import disnake

from MZscript.functions_handler import FunctionsHandler

class FuncBan(FunctionsHandler):
    def __init__(self, handler):
        super().__init__()
        self.client = handler.client
        self.bot = handler.client.bot

    async def func_ban(self, ctx: disnake.message.Message, args: str = None):
        args_list = await self.get_args(await self.is_have_functions(args, ctx))
        
        guild = ctx.guild
        if args_list[0].isdigit() and len(args_list) > 1:
            try:
                if not self.bot.get_user(int(args_list[0])):
                    guild = self.bot.get_guild(int(args_list[0]))
                else:
                    args_list.insert(0, guild)
            except Exception as e:
                print(e)
                raise SyntaxError(f"$ban: Cannot find guild \"{args_list[0]}\"")
        else:
            args_list.insert(0, guild)
        
        reason = None
        if len(args_list) > 2 and len(args_list[2]) > 0:
            reason = args_list[2]

        user = await self.bot.fetch_member(args_list[1])
        await guild.ban(user=user, reason=reason, clean_history_duration=0)

def setup(handler):
    return FuncBan(handler)