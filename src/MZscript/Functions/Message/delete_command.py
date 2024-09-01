import disnake

from ...functions_handler import FunctionsHandler


class Functions(FunctionsHandler):
    def __init__(self, handler):
        super().__init__()
        self.handler = handler
        self.bot = handler.client.bot

    async def func_deletecommand(self, ctx: disnake.Message, args: str):
        """
        `$deletecommand[(delay;format)]`
        ### Example:
        `$deletecommand[5;s]`
        """
        args_list = await self.get_args(await self.is_have_functions(args, ctx))
        if len(args_list) > 2:
            error_msg = "$deletecommand: Too many args provided"
            if self.handler.debug_console:
                raise ValueError(error_msg)
            await ctx.channel.send(error_msg)
            return True
        is_delete = None
        if len(args_list) != 0:
            try:
                float(args_list[0])
            except:
                error_msg = f"$sendMessage: #deleteIn: First argument must be number: \"{args_list[0]}\""
                if self.handler.debug_console:
                    raise ValueError(error_msg)
                await ctx.channel.send(error_msg)
                return True

            if len(args_list) > 1:
                if args_list[1] not in ['s', 'm', 'h', 'd']:
                    error_msg = f"$sendMessage: #deleteIn: Unsupported time format \"{args_list[1]}\". Select: s, m, h or d"
                    if self.handler.debug_console:
                        raise ValueError(error_msg)
                    await ctx.channel.send(error_msg)
                    return True
            else:
                args_list.append('s')
            is_delete = int(args_list[0]) * {'s': 1, 'm': 60, 'h': 60*60, 'd': 60*60*24}[args_list[1]]
        if is_delete:
            await ctx.delete(delay=int(args_list[0]) * {'s': 1, 'm': 60, 'h': 60*60, 'd': 60*60*24}[args_list[1]])
        else:
            await ctx.delete()

def setup(handler):
    return Functions(handler)