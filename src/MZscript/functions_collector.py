import disnake

from functions_handler import FunctionsHandler


class FunctionsCore(FunctionsHandler):
    def __init__(self, client, db_warns: bool = False, debug_log: bool = False):
        super().__init__(client.bot)
        self.db_warns = db_warns
        self.debug_log = debug_log
        self.client = client
        self.sync_functions()

    def sync_functions(self):
        for line in self.all_funcs:
            try:
                function = eval("self.func_"+line.replace("$", "").lower())
                self.funcs[line] = function
            except NameError as e:
                print(f"WARNING: for command \"{line}\" not exists function found.")

    async def func_if(self, ctx, args: str):
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
                vals = args.split(i)
                if i in ["==", "!="]:
                    val1 = vals[0].strip()
                    val2 = vals[1].strip()
                else:
                    val1 = int(vals[0])
                    val2 = int(vals[1])
                val1 = await self.is_have_functions(val1, ctx)
                val2 = await self.is_have_functions(val2, ctx)
                return operator_mapping.get(i, lambda x, y: None)(val1, val2)
        return False

    async def func_elif(self, ctx, args: str): # return result from $if (DRY)
        return await self.func_if(ctx, args)

    async def func_else(self, ctx): # all $else function translated to $elif[True] for better output because he have brackets
        return "$elif[True]"

    async def func_eval(self, ctx, args: str): # its unstability function. try not use it
        chunks = await self.get_chunks(args)
        for i in chunks:
            if i.startswith("$"):
                args = await self.client.run_code(args, ctx)
                return await self.client.run_code(args, ctx)
        else:
            return args

    async def func_sendmessage(self, ctx, args: str):
        args_list = await self.get_args(args)
        if len(args_list) < 1:
            raise ValueError(f"$sendMessage: Needs 1 arguments, but only {len(args_list)} provided: \"{args}\"")

        channel = ctx.channel
        if args_list[0].isdigit():
            try:
                channel = self.client.bot.get_channel(int(await self.is_have_functions(args_list[0], ctx)))
            except Exception as e:
                print(e)
                raise SyntaxError(f"$sendMessage: Cannot find channel \"{args_list[0]}\"")
        else:
            args_list.insert(0, channel)
        embed = disnake.Embed()
        content = None
        if len(args_list) > 1 and len(args_list[1]) > 0:
            content = await self.is_have_functions(args_list[1], ctx)
        if len(args_list) > 2 and len(args_list[2]) > 0:
            embed.title = await self.is_have_functions(args_list[2], ctx)
        if len(args_list) > 3 and len(args_list[3]) > 0:
            embed.description = await self.is_have_functions(args_list[3], ctx)
            if not embed.description:
                raise SyntaxError(f"$sendEmbed: Cannot send embed without description: {args}")
        if len(args_list) > 4 and len(args_list[4]) > 0:
            icon_url = None
            if len(args_list) > 5 and len(args_list[5]) > 0:
                icon_url = await self.is_have_functions(args_list[5], ctx)
            embed.set_footer(text=await self.is_have_functions(args_list[4], ctx), icon_url=icon_url)
        if len(args_list) > 6 and len(args_list[6]) > 0:
            embed.color = disnake.Colour(int("0x"+((await self.is_have_functions(args_list[6], ctx)).replace("#", "0x").replace("0x", "")), 16))
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
        view = disnake.ui.View(timeout=None)

        async def add_button(entry: str):
            args_splited = await self.get_args(entry, ctx)
            style = args_splited[0]
            label = args_splited[1]
            disabled = args_splited[2]
            custom_id = args_splited[3]
            url = None
            emoji = None
            row = None

            if style.lower() == "secondary":
                style = disnake.ButtonStyle.secondary
            elif style.lower() == "success":
                style = disnake.ButtonStyle.success
            elif style.lower() == "danger":
                style = disnake.ButtonStyle.danger
            elif style.lower() == "primary":
                style = disnake.ButtonStyle.primary
            elif style.lower() == "link":
                style = disnake.ButtonStyle.link
            else:
                raise ValueError("$sendMessage: #addButton: Style incorrect type\n\nPlease, select secondary/success/danger/primary or link type.")
            view.add_item(disnake.ui.Button(style=style, label=label, disabled=disabled.lower() == "true", custom_id=custom_id, url=url, emoji=emoji, row=row))

        async def add_field(entry: str):
            args_splited = await self.get_args(await self.is_have_functions(entry), ctx)
            if len(args_splited) < 2:
                raise ValueError("$sendMessage: #addField: Name and value of field are required.")
            inline = False
            if len(args_splited) > 2:
                inline = args_splited[2].lower() == "true"
            embed.add_field(args_splited[0], args_splited[1], inline=inline)

        if len(args_list) > 12:
            tag_funcs = {
                "#addfield": add_field,
                "#addbutton": add_button,
                }
            for tag in tag_funcs.keys():
                for i in args_list[11:]:
                    if i.lower().startswith(tag):
                        await tag_funcs[tag](i[len(tag)+1:-1])
        if not embed.description:
            embed = None
        await channel.send(content=content, embed=embed, view=view)

    async def func_message(self, ctx: disnake.message.Message, args: str = ""):
        if len(args) == 0:
            return ctx.content
        return ctx.content.split(" ")[int(args)]

    async def func_channelinfo(self, ctx: disnake.message.Message, args: str):
        args = await self.is_have_functions(args, ctx)
        args_list = await self.get_args(args, ctx)
        if len(args_list) > 2 or len(args_list) == 0:
            raise ValueError("$channelInfo: To many or no args provided")
        channel = ctx.channel
        if args_list[0].isdigit():
            try:
                channel = self.client.bot.get_channel(int(await self.is_have_functions(args_list[0], ctx)))
            except Exception as e:
                print(e)
                raise SyntaxError(f"$channelInfo: Cannot find channel \"{args_list[0]}\"")
        else:
            args_list.insert(0, channel)
        params = {
            "name": channel.name,
            "guild": channel.guild.id,
            "id": channel.id,
            "category_id": channel.category_id,
            "topic": channel.topic,
            "position": channel.position,
            "last_message": channel.last_message_id,
            "slowmode_delay": channel.slowmode_delay,
            "thread_slowmode": channel.default_thread_slowmode_delay,
            "nsfw": str(channel.nsfw).lower(),
            "auto_archive_duration": channel.default_auto_archive_duration
            }
        return str(params[args_list[1]])

    async def func_text(self, ctx: disnake.message.Message, args: str):
        return args

    async def func_customid(self, ctx: disnake.MessageInteraction, args: str = None):
        return ctx.component.custom_id

    async def func_defer(self, ctx: disnake.MessageInteraction, args: str = None):
        await ctx.response.defer()
        return ""

    async def func_getvar(self, ctx, args: str):
        result = await self.database.get_global_var(await self.is_have_functions(args, ctx))
        if result:
            return result
        elif self.db_warns:
            print(f"WARNING: Value for global var \"{args}\" not provided (returning empty string)")
        return ""

    async def func_setvar(self, ctx, args: str):
        args_list = await self.get_args(await self.is_have_functions(args, ctx))
        if len(args_list) < 2:
            raise ValueError(f"$setVar needs 2 arguments, but only {len(args_list)} provided: \"{args}\"")
        await self.database.set_global_var(args_list[0], args_list[1])

    async def func_delvar(self, ctx, args: str):
        args_list = await self.get_args(await self.is_have_functions(args, ctx))
        if len(args_list) < 1:
            raise ValueError(f"$setVar needs 1 arguments, but only {len(args_list)} provided: \"{args}\"")
        await self.database.set_global_var(args_list[0])

    async def func_getmembervar(self, ctx, args: str):
        args_list = await self.get_args(await self.is_have_functions(args, ctx))
        if len(args_list) < 1:
            raise ValueError(f"$getMemberVar needs 1 arguments, but only {len(args_list)} provided: \"{args}\"")
        if len(args_list) == 1:
            args_list.append(ctx.author.id)
        if len(args_list) == 2:
            args_list.append(ctx.guild.id)
        result = await self.database.get_value_from_member(args_list[2], args_list[1], args_list[0])
        if result:
            return result
        elif self.db_warns:
            print(f"WARNING: Value for member var \"{args_list[0]}\" not provided (returning empty string)")
        return ""

    async def func_setmembervar(self, ctx, args: str):
        args_list = await self.get_args(await self.is_have_functions(args, ctx))
        if len(args_list) < 2:
            raise ValueError(f"$setMemberVar needs 2 arguments, but only {len(args_list)} provided: \"{args}\"")
        if len(args_list) == 2:
            args_list.append(ctx.author.id)
        if len(args_list) == 3:
            args_list.append(ctx.guild.id)
        await self.database.set_value_of_member(args_list[3], args_list[2], args_list[0], args_list[1])

    async def func_delmembervar(self, ctx, args: str):
        args_list = await self.get_args(await self.is_have_functions(args, ctx))
        if len(args_list) < 1:
            raise ValueError(f"$detMemberVar needs 2 arguments, but only {len(args_list)} provided: \"{args}\"")
        if len(args_list) == 1:
            args_list.append(ctx.author.id)
        if len(args_list) == 2:
            args_list.append(ctx.guild.id)
        await self.database.del_value_of_member(args_list[2], args_list[1], args_list[0])

    async def func_getguildvar(self, ctx, args: str):
        args_list = await self.get_args(await self.is_have_functions(args, ctx))
        if len(args_list) < 1:
            raise ValueError(f"$getGuildVar needs 1 arguments, but only {len(args_list)} provided: \"{args}\"")
        if len(args_list) == 1:
            args_list.append(ctx.guild.id)
        result = await self.database.get_value_from_guild(args_list[1], args_list[0])
        if result:
            return result
        elif self.db_warns:
            print(f"WARNING: Value for guild var \"{args_list[0]}\" not provided (returning empty string)")
        return ""

    async def func_setguildvar(self, ctx, args: str):
        args_list = await self.get_args(await self.is_have_functions(args, ctx))
        if len(args_list) < 2:
            raise ValueError(f"$setVar needs 2 arguments, but only {len(args_list)} provided: \"{args}\"")
        if len(args_list) == 2:
            args_list.append(ctx.guild.id)
        await self.database.set_value_of_guild(args_list[2], args_list[0], args_list[1])

    async def func_delguildvar(self, ctx, args: str):
        args_list = await self.get_args(await self.is_have_functions(args, ctx))
        if len(args_list) < 1:
            raise ValueError(f"$setVar needs 1 arguments, but only {len(args_list)} provided: \"{args}\"")
        if len(args_list) == 1:
            args_list.append(ctx.guild.id)
        await self.database.del_value_of_guild(args_list[1], args_list[0])

    async def func_getuservar(self, ctx, args: str):
        args_list = await self.get_args(await self.is_have_functions(args, ctx))
        if len(args_list) < 1:
            raise ValueError(f"$getUserVar needs 1 arguments, but only {len(args_list)} provided: \"{args}\"")
        if len(args_list) == 1:
            args_list.append(ctx.author.id)
        result = await self.database.get_value_from_user(args_list[1], args_list[0])
        if result:
            return result
        elif self.db_warns:
            print(f"WARNING: Value for user var \"{args_list[0]}\" not provided (returning empty string)")
        return ""

    async def func_setuservar(self, ctx, args: str):
        args_list = await self.get_args(await self.is_have_functions(args, ctx))
        if len(args_list) < 2:
            raise ValueError(f"$setUserVar needs 2 arguments, but only {len(args_list)} provided: \"{args}\"")
        if len(args_list) == 2:
            args_list.append(ctx.author.id)
        await self.database.set_value_of_user(args_list[2], args_list[0], args_list[1])

    async def func_deluservar(self, ctx, args: str):
        args_list = await self.get_args(await self.is_have_functions(args, ctx))
        if len(args_list) < 1:
            raise ValueError(f"$setUserVar needs 1 arguments, but only {len(args_list)} provided: \"{args}\"")
        if len(args_list) == 1:
            args_list.append(ctx.author.id)
        await self.database.del_value_of_user(args_list[1], args_list[0])

    async def func_updatecommands(self, ctx, args: str):
        await self.client.update_commands()

    async def func_calculate(self, ctx, args: str):
        args = await self.is_have_functions(args, ctx)
        from ast import parse, walk, Name

        def check_expression(expression):
            for node in walk(parse(expression, mode='eval')):
                if isinstance(node, Name):
                    return False
            return True

        if check_expression(args.strip()):
            return str(eval(args.strip()))
        else:
            raise SyntaxError(f"$calculate: Cannot calculate provided expression: {args}")

    async def func_console(self, ctx, args: str = None):
        if args is None or len(args) == 0:
            return
        print(await self.is_have_functions(args, ctx))