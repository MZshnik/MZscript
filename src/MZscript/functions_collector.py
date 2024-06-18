import disnake
from disnake.ext import commands

from functions_handler import FunctionsHandler


class FunctionsCore(FunctionsHandler):
    def __init__(self, client):
        super().__init__(client.bot)
        self.client = client
        self.sync_functions()

    def sync_functions(self):
        for line in self.all_funcs:
            try:
                function = eval("self.func_"+line.replace("$", "").lower())
                self.funcs[line] = function
            except NameError as e:
                print(f"WARNING: for command \"{line}\" not exists function found.")

    async def func_if(self, ctx: disnake.message.Message, args: str):
        if args.lower() == "true":
            return True
        elif args.lower() == "false":
            return False
        choices = ["==", ">=", "<=", "!=", "<", ">"]
        operator_mapping = {
            "==": lambda x, y: x == y,
            "!=": lambda x, y: x != y,
            ">": lambda x, y: x > y,
            ">=": lambda x, y: x >= y,
            "<": lambda x, y: x < y,
            "<=": lambda x, y: x <= y,
        }
        for i in choices:
            if i in args:
                if i in ["==", "!="]:
                    vals = args.split(i)
                    val1 = vals[0].strip()
                    val2 = vals[1].strip()
                else:
                    vals = args.split(i)
                    val1 = int(vals[0])
                    val2 = int(vals[1])
                val1 = await self.is_have_functions(val1, ctx)
                val2 = await self.is_have_functions(val2, ctx)
                if operator_mapping.get(i, lambda x, y: None)(val1, val2):
                    return True
                else:
                    return False
        return False

    async def func_elif(self, ctx: disnake.message.Message, args: str): # return result from $if (DRY)
        return await self.func_if(ctx, args)

    async def func_else(self, ctx: disnake.message.Message): # all $else function translated to $elif[True] for better output because he have brackets
        return "$elif[True]"

    async def func_stop(self, ctx: disnake.message.Message): # nvm, this function will be made in the future
        return "STOPIT"

    async def func_eval(self, ctx: disnake.message.Message, args: str): # its unstability function. try not use it
        chunks = await self.get_chunks(args)
        for i in chunks:
            if i.startswith("$"):
                args = await self.client.run_code(args, ctx)
                args = await self.client.run_code(args, ctx)
                return args
        else:
            return args

    async def func_sendmessage(self, ctx: disnake.message.Message, args: str): # send message to provided channel or ctx
        try:
            args_list = await self.get_args(args)
            if len(args_list) == 2:
                channel = ctx.guild.get_channel(int(await self.is_have_functions(args_list[0], ctx)))
                if channel:
                    await channel.send(await self.is_have_functions(args_list[1], ctx))
                else:
                    raise SyntaxError(f"Can't find channel \"{args_list[0]}\"")
            elif len(args_list) == 1:
                result = await self.is_have_functions(args_list[0], ctx)
                await ctx.channel.send(result)
        except Exception as e:
            raise SyntaxError("$sendMessage: Cannot send empty message")

    async def func_sendembed(self, ctx: disnake.message.Message, args: str):
        args_list = await self.get_args(args)
        if len(args_list) < 1:
            raise ValueError(f"$sendEmbed needs 1 arguments, but only {len(args_list)} provided: \"{args}\"")

        channel = ctx.channel
        if isinstance(args_list[0], int):
            try:
                channel = ctx.guild.get_channel(int(await self.is_have_functions(args_list[0], ctx)))
                args_list.insert(0, channel)
            except Exception as e:
                print(e)
                raise SyntaxError(f"Cannot find channel \"{args_list[0]}\"")
        embed = disnake.Embed()
        content = None
        if len(args_list) > 1 and len(args_list[1]) > 0:
            content = await self.is_have_functions(args_list[1], ctx)
        if len(args_list) > 2 and len(args_list[2]) > 0:
            embed.title = await self.is_have_functions(args_list[2], ctx)
        if len(args_list) > 3 and len(args_list[3]) > 0:
            embed.description = await self.is_have_functions(args_list[3], ctx)
        if len(args_list) > 4 and len(args_list[4]) > 0:
            icon_url = None
            if len(args_list) > 5 and len(args_list[5]) > 0:
                icon_url = await self.is_have_functions(args_list[5], ctx)
            embed.set_footer(await self.is_have_functions(args_list[4], ctx), icon_url)
        if len(args_list) > 6 and len(args_list[6]) > 0:
            try:
                embed.color = disnake.Colour(int((await self.is_have_functions(args_list[6], ctx)).replace("#", "0x"), 16))
            except:
                embed.color = disnake.Colour(int("0x"+(await self.is_have_functions(args_list[6], ctx)).replace("#", ""), 16))
        if len(args_list) > 7 and len(args_list[7]) > 0:
            embed.set_thumbnail(await self.is_have_functions(args_list[7], ctx))
        if len(args_list) > 8 and len(args_list[8]) > 0:
            embed.set_image(await self.is_have_functions(args_list[8], ctx))
        if len(args_list) > 9 and len(args_list[9]) > 0:
            url = None
            if len(args_list) > 10 and len(args_list[10]) > 0:
                url = await self.is_have_functions(args_list[10], ctx)
            icon_url = None
            if len(args_list) > 11 and len(args_list[11]) > 0:
                icon_url = await self.is_have_functions(args_list[11], ctx)
            embed.set_author(name=await self.is_have_functions(args_list[9], ctx), url=url, icon_url=icon_url)
        if not embed.description:
            raise SyntaxError(f"Cannot send embed without description: {args}")
        if content:
            await channel.send(content=content, embed=embed)
        else:
            await channel.send(embed=embed)

    async def func_message(self, ctx: disnake.message.Message, args: str = ""):
        if len(args) == 0:
            return ctx.content
        return ctx.content.split(" ")[int(args)]

    async def func_addbutton(self, ctx: disnake.message.Message, args: str): # test and fun function
        print(f"addButton with args: {args}")
        return "penis is good"

    async def func_channelinfo(self, ctx: disnake.message.Message, args: str):
        return str(ctx.channel.id)

    async def func_text(self, ctx: disnake.message.Message, args: str):
        return args

    async def func_getvar(self, ctx: disnake.message.Message, args: str):
        result = await self.is_have_functions(args, ctx)
        result = await self.database.get_global_var(result)
        if result:
            return result
        else:
            print(f"WARNING: Value for global var \"{args}\" not provided (returning empty string)")
            return ""

    async def func_setvar(self, ctx: disnake.message.Message, args: str):
        args_list = await self.get_args(args)
        count = 0
        for i in args_list:
            args_list[count] = await self.is_have_functions(i, ctx)
            count += 1
        if len(args_list) < 2:
            raise ValueError(f"$setVar needs 2 arguments, but only {len(args_list)} provided: \"{args}\"")
        await self.database.set_global_var(args_list[0], args_list[1])

    async def func_getmembervar(self, ctx: disnake.message.Message, args: str):
        args_list = await self.get_args(args)
        count = 0
        for i in args_list:
            args_list[count] = await self.is_have_functions(i, ctx)
            count += 1
        if len(args_list) < 1:
            raise ValueError(f"$getMemberVar needs 1 arguments, but only {len(args_list)} provided: \"{args}\"")
        if len(args_list) == 1:
            args_list.append(ctx.author.id)
        if len(args_list) == 2:
            args_list.append(ctx.guild.id)
        result = await self.database.get_value_from_member(args_list[2], args_list[1], args_list[0])
        if result:
            return result
        else:
            print(f"WARNING: Value for member var \"{args_list[0]}\" not provided (returning empty string)")
            return ""

    async def func_setmembervar(self, ctx: disnake.message.Message, args: str):
        args_list = await self.get_args(args)
        count = 0
        for i in args_list:
            args_list[count] = await self.is_have_functions(i, ctx)
            count += 1
        if len(args_list) < 2:
            raise ValueError(f"$setMemberVar needs 2 arguments, but only {len(args_list)} provided: \"{args}\"")
        if len(args_list) == 2:
            args_list.append(ctx.author.id)
        if len(args_list) == 3:
            args_list.append(ctx.guild.id)
        await self.database.set_value_of_member(args_list[3], args_list[2], args_list[0], args_list[1])

    async def func_getguildvar(self, ctx: disnake.message.Message, args: str):
        args_list = await self.get_args(args)
        count = 0
        for i in args_list:
            args_list[count] = await self.is_have_functions(i, ctx)
            count += 1
        if len(args_list) < 1:
            raise ValueError(f"$getGuildVar needs 1 arguments, but only {len(args_list)} provided: \"{args}\"")
        if len(args_list) == 1:
            args_list.append(ctx.guild.id)
        result = await self.database.get_value_from_guild(args_list[1], args_list[0])
        if result:
            return result
        else:
            print(f"WARNING: Value for guild var \"{args_list[0]}\" not provided (returning empty string)")
            return ""

    async def func_setguildvar(self, ctx: disnake.message.Message, args: str):
        args_list = await self.get_args(args)
        count = 0
        for i in args_list:
            args_list[count] = await self.is_have_functions(i, ctx)
            count += 1
        if len(args_list) < 2:
            raise ValueError(f"$setVar needs 2 arguments, but only {len(args_list)} provided: \"{args}\"")
        if len(args_list) == 2:
            args_list.append(ctx.guild.id)
        await self.database.set_value_of_guild(args_list[2], args_list[0], args_list[1])

    async def func_getuservar(self, ctx: disnake.message.Message, args: str):
        args_list = await self.get_args(args)
        count = 0
        for i in args_list:
            args_list[count] = await self.is_have_functions(i, ctx)
            count += 1
        if len(args_list) < 1:
            raise ValueError(f"$getUserVar needs 1 arguments, but only {len(args_list)} provided: \"{args}\"")
        if len(args_list) == 1:
            args_list.append(ctx.author.id)
        result = await self.database.get_value_from_user(args_list[1], args_list[0])
        if result:
            return result
        else:
            print(f"WARNING: Value for user var \"{args_list[0]}\" not provided (returning empty string)")
            return ""

    async def func_setuservar(self, ctx: disnake.message.Message, args: str):
        args_list = await self.get_args(args)
        count = 0
        for i in args_list:
            args_list[count] = await self.is_have_functions(i, ctx)
            count += 1
        if len(args_list) < 2:
            raise ValueError(f"$setUserVar needs 2 arguments, but only {len(args_list)} provided: \"{args}\"")
        if len(args_list) == 2:
            args_list.append(ctx.author.id)
        await self.database.set_value_of_user(args_list[2], args_list[0], args_list[1])

    async def func_updatecommands(self, ctx: disnake.message.Message, args: str):
        await self.client.update_commands()

    async def func_console(self, ctx: disnake.message.Message = None, args: str = None):
        if args is None or len(args) == 0:
            return
        print(await self.is_have_functions(args, ctx))