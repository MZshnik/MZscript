import disnake

from ...functions_handler import FunctionsHandler


class Functions(FunctionsHandler):
    def __init__(self, handler):
        super().__init__()
        self.handler = handler
        self.bot = handler.client.bot

    async def func_replacetext(self, ctx: disnake.message.Message, args: str):
        args_list = await self.get_args(await self.is_have_functions(args, ctx))
        if len(args_list) < 3:
            raise ValueError(f"$replaceText: Needs 3 arguments, but only {len(args_list)} provided: \"{args}\"")
        if len(args_list) > 4:
            raise ValueError(f"$replaceText: Too many args provided")
        if len(args_list) > 3:
            if args_list[3].isdigit():
                return args_list[0].replace(args_list[1], args_list[2], args_list[3])
            else:
                raise ValueError(f"$replaceText: Cannot replace \"{args_list[1]}\" to \"{args_list[2]}\" in provided text \"{args_list[3]}\" times: \"{args}\"")
        return args_list[0].replace(args_list[1], args_list[2])

def setup(handler):
    return Functions(handler)