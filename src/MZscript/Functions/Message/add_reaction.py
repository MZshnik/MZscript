import disnake

from ...functions_handler import FunctionsHandler


class AddReaction(FunctionsHandler):
    def __init__(self, handler):
        super().__init__()
        self.handler = handler
        self.bot = handler.client.bot

    async def func_addreaction(self, ctx: disnake.Message, args: str):
        """
        `$addReaction[(channel;message);emoji]`
        #### Example:
        `$addReaction[😎]`
        """
        args_list = await self.get_args(await self.is_have_functions(args, ctx))
        if len(args_list) > 3 or len(args_list) == 0:
            raise ValueError("$addReaction: Too many or no args provided")

        channel = ctx.channel
        if args_list[0].isdigit() and len(args_list) > 1:
            try:
                if not self.bot.get_message(int(args_list[0])):
                    channel = self.bot.get_channel(int(args_list[0]))
                else:
                    args_list.insert(0, channel)
            except:
                raise SyntaxError(f"$addReaction: Cannot find channel \"{args_list[0]}\"")
        else:
            args_list.insert(0, channel)

        message = ctx
        if args_list[1].isdigit() and len(args_list) > 2:
            try:
                message = self.bot.get_message(int(args_list[1]))
                if not message:
                    message = await channel.fetch_message(int(args_list[1]))
                if not message:
                    message = ctx
                    args_list.insert(1, message)
            except:
                raise SyntaxError(f"$addReaction: Cannot find message \"{args_list[1]}\"")
        else:
            args_list.insert(1, message)

        await message.add_reaction(emoji=args_list[2])

def setup(handler):
    return AddReaction(handler)