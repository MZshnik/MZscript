import asyncio
import random

import disnake

from ..functions_handler import FunctionsHandler
from datetime import datetime


class Functions(FunctionsHandler):
    def __init__(self, handler):
        super().__init__()
        self.handler = handler
        self.bot = handler.client.bot

    async def func_message(self, ctx: disnake.Message, args: str = ""):
        """
        `$message[(arg number)]`
        ### Example:
        `$message`
        ### Example 2:
        `$message[0]`
        """
        if len(args) == 0:
            return ctx.content
        return ctx.content.split(" ")[int(args)]

    async def func_text(self, ctx: disnake.Message, args: str):
        """
        `$text[text]`
        ### Example:
        `$text[$sendMessage[this function like text]]`
        """
        return args

    async def func_customid(self, ctx: disnake.MessageInteraction, args: str = None):
        """
        `$customID`\n
        No args. Return $customID of component
        ### Example:
        `$if[$customID==button1] $sendMessage[Button pressed] $endif`
        """
        return ctx.component.custom_id

    async def func_value(self, ctx: disnake.MessageInteraction, args: str = None):
        if args and len(args) != 0:
            return ctx.values[int(await self.get_args(await self.is_have_functions(args)))]
        return ctx.values[0]

    async def func_options(self, inter: disnake.AppCmdInter, args: str = None):
        # print("Options:")
        # print(inter.data.options)
        return inter.data.options

    async def func_defer(self, ctx: disnake.MessageInteraction, args: str = None):
        """
        `$defer`\n
        No args. Defer interaction
        ### Example:
        `$defer $sendMessage[Button pressed]`
        """
        await ctx.response.defer()
        return ""

    async def func_bottyping(self, ctx, args: str):
        """
        `$botTyping[(guild;channel);delay]`
        """
        args_list = await self.get_args(await self.is_have_functions(args, ctx), ctx)
        if len(args_list) > 3 or len(args_list) == 0:
            error_msg = "$botTyping: Too many or no args provided"
            if self.handler.debug_console:
                raise ValueError(error_msg)
            await ctx.channel.send(error_msg)
            return True

        guild = ctx.guild
        if len(args_list) > 2:
            if not args_list[0].isdigit():
                error_msg = f"$botTyping: Cannot find guild \"{args_list[0]}\""
                if self.handler.debug_console:
                    raise SyntaxError(error_msg)
                await ctx.channel.send(error_msg)
                return True
            guild = self.bot.get_guild(int(args_list[0]))
            if not guild:
                guild = await self.bot.fetch_guild(int(args_list[0]))
            if not guild:
                error_msg = f"$botTyping: Cannot find guild \"{args_list[0]}\""
                if self.handler.debug_console:
                    raise SyntaxError(error_msg)
                await ctx.channel.send(error_msg)
                return True
        else:
            args_list.insert(0, guild)

        channel = ctx.channel
        if len(args_list) > 2:
            if not args_list[1].isdigit():
                error_msg = f"$botTyping: Channel id must be integer \"{args_list[1]}\""
                if self.handler.debug_console:
                    raise SyntaxError(error_msg)
                await ctx.channel.send(error_msg)
                return True

            channel = guild.get_channel(int(args_list[1]))
            if not channel:
                channel = await guild.fetch_channel(int(args_list[1]))
            if not channel:
                error_msg = f"$botTyping: Cannot find channel \"{args_list[0]}\""
                if self.handler.debug_console:
                    raise SyntaxError(error_msg)
                await ctx.channel.send(error_msg)
                return True
        else:
            args_list.insert(1, ctx.channel)

        try:
            float(args_list[2])
        except:
            error_msg = f"$botTyping: Delay must be number: \"{args_list[2]}\""
            if self.handler.debug_console:
                raise ValueError(error_msg)
            await ctx.channel.send(error_msg)
            return True

        async with channel.typing():
            await asyncio.sleep(float(args_list[2]))

    async def func_random(self, ctx, args: str):
        """
        `$random[start;stop;(step;float numbers count)]`
        ### Example:
        `$random[0;100]`
        """
        args_list = await self.get_args(await self.is_have_functions(args))
        if len(args_list) > 4 or len(args_list) == 0:
            error_msg = "$random: Too many or no args provided"
            if self.handler.debug_console:
                raise ValueError(error_msg)
            await ctx.channel.send(error_msg)
            return True

        # TODO: Make support of float numbers

        if len(args_list) < 3:
            args_list.insert(2, 1)
        elif len(args_list[2]) > 0:
            is_float = False
            # try:
            #     float(args_list[2])
            #     is_float = True
            # except:
            #     pass

            if not args_list[2].isdigit() and not is_float:
                error_msg = f"$random: Third argument must be number: \"{args_list[2]}\""
                if self.handler.debug_console:
                    raise ValueError(error_msg)
                await ctx.channel.send(error_msg)
                return True

        if len(args_list) < 4:
            args_list.insert(3, 1)
        elif len(args_list[3]) > 0:
            is_float = False
            # try:
            #     float(args_list[2])
            #     is_float = True
            # except:
            #     pass

            if not args_list[3].isdigit() and not is_float:
                error_msg = f"$random: Fourth argument must be number: \"{args_list[3]}\""
                if self.handler.debug_console:
                    raise ValueError(error_msg)
                await ctx.channel.send(error_msg)
                return True

        return str(round(random.randrange(
            int(args_list[0]), int(args_list[1]),
            int(args_list[2])), int(args_list[3])
            ))

    async def func_calculate(self, ctx, args: str):
        """
        `$calculate[expression]`
        ### Example:
        `$calculate[1+1]`
        ### Example 2:
        `$calculate[$getVar[commands]+1]`
        ### Example 3:
        `$calculate[2*2]`
        ### Example 4:
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
                # TODO: Add support in future:
                from math import sqrt, ceil, floor
                return str(eval(args.strip()))
            except:
                raise SyntaxError(f"$calculate: Cannot calculate provided expression: {args}")
        else:
            raise SyntaxError(f"$calculate: Cannot calculate provided expression: {args}")

    async def func_gettimestamp(self, ctx, args: str = None):
        return str(int(datetime.now().timestamp()))

    async def func_wait(self, ctx, args: str):
        """
        `$wait[delay;(format)]`
        ### Example:
        `$wait[2]`
        ### Example 2:
        `$wait[1;m]`
        ### Example 3:
        `$wait[30;s]`
        """
        args_list = await self.get_args(await self.is_have_functions(args))
        if len(args_list) > 2 or len(args_list) == 0:
            error_msg = "$wait: Too many or no args provided"
            if self.handler.debug_console:
                raise ValueError(error_msg)
            await ctx.channel.send(error_msg)
            return True

        is_float = False
        try:
            float(args_list[0])
            is_float = True
        except:
            pass

        if not args_list[0].isdigit() and not is_float:
            error_msg = f"$wait: First argument must be number: \"{args_list[0]}\""
            if self.handler.debug_console:
                raise ValueError(error_msg)
            await ctx.channel.send(error_msg)
            return True

        if len(args_list) > 1:
            if args_list[1] not in ['s', 'm', 'h', 'd']:
                error_msg = f"$wait: Unsupported time format \"{args_list[1]}\". Select: s, m, h or d"
                if self.handler.debug_console:
                    raise ValueError(error_msg)
                await ctx.channel.send(error_msg)
                return True
        else:
            args_list.append('s')

        await asyncio.sleep(int(args_list[0]) * {'s': 1, 'm': 60, 'h': 60*60, 'd': 60*60*24}[args_list[1]])

    async def func_loop(self, ctx, args: str):
        """
        `$loop[condition;iteration code]`
        ### Example:
        `$var[set;msg;1]`\n
        `$loop[$var[msg]==11111;`\n
        `$var[set;gay;$var[msg]1]]`\n
        `$sendMessage[$var[msg]]`
        """
        args_list = await self.get_args(args, ctx)
        if len(args_list) != 3:
            error_msg = f"$loop: Too many or no args provided"
            if self.handler.debug_console:
                raise ValueError(error_msg)
            await ctx.channel.send(error_msg)
            return True

        iteration_if = args_list[0]
        iteration_message = args_list[1]
        while (await self.is_have_functions(f"$if[{iteration_if}] $text[true] $else $text[false] $endif", ctx)).strip() == "false":
            result = await self.is_have_functions(iteration_message, ctx)
        return result if result else ""

    async def func_for(self, ctx, args: str):
        """
        `$for[iterator name;list;iteration code]`
        ### Example:
        `$for[i;`\n
        `$var[somelist];`\n
        `$console[$var[i]]]`
        """
        args_list = await self.get_args(args, ctx)
        if len(args_list) != 3:
            error_msg = f"$for: Too many or no args provided"
            if self.handler.debug_console:
                raise ValueError(error_msg)
            await ctx.channel.send(error_msg)
            return True

        result = await self.is_have_functions(args_list[1])
        for i in list(result):
            await self.handler.database.set_json_var(args_list[0], i)
            await self.is_have_functions(args_list[2])
        await self.handler.database.del_json_var(args_list[0])
        return ""

    async def func_updatecommands(self, ctx, args: str = None):
        """
        `$updateCommands`\n
        No args. Returns nothing. Update code of command triggers
        ### Example:
        `$updateCommands $sendMessage[Commands updated]`
        """
        await self.handler.client.update_commands()

    async def func_uptime(self, ctx, args: str = None):
        """
        `$uptime`
        No args. Returns timestamp uptime of bot working
        ### Example:
        `$sendMessage[Uptime: $uptime]`
        """
        return self.handler.python_vars["uptime"]

    async def func_docs(self, ctx, args: str):
        """
        `$docs[$func]`
        ### Example:
        `$docs[docs]`
        """
        import re
        func = re.sub(r"\[\[|\]\]", "", (await self.is_have_functions(args, ctx)).lower())
        if "$"+func in self.funcs:
            docs = self.funcs["$"+func].__doc__
            docs = docs.replace("    ", "")
            return self.funcs["$"+func].__doc__.replace("    ", "")
        else:
            return ""

    async def func_console(self, ctx, args: str = None):
        """
        `$console[message]`
        ### Example:
        `$console[Bot is ready]`
        """
        if args is None or len(args) == 0:
            return ""
        print(await self.is_have_functions(args, ctx))

def setup(handler):
    return Functions(handler)