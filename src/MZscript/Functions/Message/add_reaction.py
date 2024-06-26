import disnake

from src.MZscript.functions_handler import FunctionsHandler

class AddReaction(FunctionsHandler):
    def __init__(self, handler):
        super().__init__()
        self.client = handler.client
        self.bot = handler.client.bot

	# [channelid?;messageid;emoji]
    async def func_addreaction(self, ctx, args: str):
        args_list = await self.get_args(await self.is_have_functions(args, ctx))

        guild = ctx.guild
        if args_list[0].isdigit() and len(args_list) > 2:
            try:
                if not self.bot.get_channel(int(args_list[0])):
                    guild = self.bot.get_guild(int(args_list[0]))
                args_list.insert(0, guild)
            except:
                raise SyntaxError(f'$addReaction: Cannot find guild "{args_list[0]}"')
        else:
            args_list.insert(0, guild)

        channel = disnake.utils.get(ctx.guild.text_channels, id=ctx.channel.id)
        if len(args_list) > 3 and len(args_list[1]) > 0:
            channel = disnake.utils.get(ctx.guild.text_channels, id=int(args_list[1]))
            args_list[1] = channel
        else:
            args_list.insert(1, channel)
        message = await channel.fetch_message(int(args_list[2]))

        await message.add_reaction(emoji=args_list[3])

def setup(handler):
    return AddReaction(handler)