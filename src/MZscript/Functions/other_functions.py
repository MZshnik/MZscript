import disnake

from ..functions_handler import FunctionsHandler


class Functions(FunctionsHandler):
    def __init__(self, handler):
        super().__init__()
        self.handler = handler
        self.bot = handler.client.bot

    async def func_message(self, ctx: disnake.Message, args: str = ""):
        """
        `$message[(arg number)]`
        #### Example:
        `$message`
        #### Example 2:
        `$message[0]`
        """
        if len(args) == 0:
            return ctx.content
        return ctx.content.split(" ")[int(args)]

    async def func_text(self, ctx: disnake.Message, args: str):
        """
        `$text[text]`
        #### Example:
        `$text[$sendMessage[this function like text]]`
        """
        return args

    async def func_customid(self, ctx: disnake.MessageInteraction, args: str = None):
        """
        `$customID`\n
        No args. Return $customID of component
        #### Example:
        `$if[$customID==button1] $sendMessage[Button pressed] $endif`
        """
        return ctx.component.custom_id

    async def func_value(self, ctx: disnake.MessageInteraction, args: str = None):
        if args and len(args) != 0:
            return ctx.values[int(await self.get_args(await self.is_have_functions(args)))]
        return ctx.values[0]

    async def func_defer(self, ctx: disnake.MessageInteraction, args: str = None):
        """
        `$defer`\n
        No args. Defer interaction
        #### Example:
        `$defer $sendMessage[Button pressed]`
        """
        await ctx.response.defer()
        return ""

    async def func_updatecommands(self, ctx, args: str = None):
        """
        `$updateCommands`\n
        No args. Return nothing. Update code of command triggers
        #### Example:
        `$updateCommands $sendMessage[Commands updated]`
        """
        await self.handler.client.update_commands()

    async def func_calculate(self, ctx, args: str):
        """
        `$calculate[expression]`
        #### Example:
        `$calculate[1+1]`
        #### Example 2:
        `$calculate[$getVar[commands]+1]`
        #### Example 3:
        `$calculate[2*2]`
        #### Example 4:
        `$calculate[5*3/3+1]`
        """
        args = await self.is_have_functions(args, ctx)
        from ast import Name, parse, walk

        def check_expression(expression):
            for node in walk(parse(expression, mode="eval")):
                if isinstance(node, Name):
                    return False
            return True

        if check_expression(args.strip()):
            try:
                # add support in future
                from math import sqrt, ceil, floor
                return str(eval(args.strip()))
            except:
                raise SyntaxError(f"$calculate: Cannot calculate provided expression: {args}")
        else:
            raise SyntaxError(f"$calculate: Cannot calculate provided expression: {args}")

    async def func_console(self, ctx, args: str = None):
        """
        `$console[message]`
        #### Example:
        `$console[Bot is ready]`
        """
        if args is None or len(args) == 0:
            return
        print(await self.is_have_functions(args, ctx))

def setup(handler):
    return Functions(handler)