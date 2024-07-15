import disnake

from ...functions_handler import FunctionsHandler


class FuncClear(FunctionsHandler):
    def __init__(self, handler):
        super().__init__()
        self.handler = handler
        self.bot = handler.client.bot

    async def func_clear(self, ctx: disnake.Message, args: str):
        """
        `$clear[(channel);count]`
        ### Example:
        `$clear[100]`
        """
        args_list = await self.get_args(await self.is_have_functions(args))
        if len(args_list) > 2 or len(args_list) == 0:
            error_msg = "$clear: Too many or no args provided"
            if self.handler.debug_console:
                raise ValueError(error_msg)
            else:
                await ctx.channel.send(error_msg)
                return True

        channel = ctx.channel
        if len(args_list) > 1:
            channel = self.bot.get_channel(int(await self.is_have_functions(args_list[0], ctx)))
            if not channel:
                channel = await self.bot.fetch_channel(args_list[0])
            if not channel:
                error_msg = f"$clear: Cannot find channel \"{args_list[0]}\""
                if self.handler.debug_console:
                    raise SyntaxError(error_msg)
                else:
                    await ctx.channel.send(error_msg)
                    return True
        else:
            args_list.insert(0, channel)

        if not args_list[1].isdigit():
            error_msg = f"$clear: First argument must be number: \"{args_list[0]}\""
            if self.handler.debug_console:
                raise ValueError(error_msg)
            await ctx.channel.send(error_msg)
            return True
        
        count = int(args_list[1])

        while count > 0:
            if count > 100:
                await channel.purge(limit=100)
                count -= 100
            else:
                await channel.purge(limit=count)
                break

def setup(handler):
    return FuncClear(handler)