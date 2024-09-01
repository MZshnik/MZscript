import disnake

from ...functions_handler import FunctionsHandler


class Functions(FunctionsHandler):
    def __init__(self, handler):
        super().__init__()
        self.handler = handler
        self.bot = handler.client.bot

    async def func_sendmessage(self, ctx: disnake.Message, args: str):
        """
        `$sendMessage[(channel;content;title;description;footer;footer icon;color;thumbnail;image;author;author url;author icon;return id or is ephemeral)]`
        ### Example:
        `$sendMessage[hello]`
        ### Example 2:
        `$sendMessage[$userInfo[dm];;Welcome!;Welcome to new guild "$guildInfo[name]";;;0058CF]`
        """
        args_list = await self.get_args(await self.is_have_functions(args, ctx))
        if len(args_list) < 1:
            error_msg = f"$sendMessage: Too many or no args provided"
            if self.handler.debug_console:
                raise ValueError(error_msg)
            else:
                await ctx.channel.send(error_msg)
                return True

        channel = ctx.channel
        if args_list[0].isdigit() and len(args_list) > 1:
            channel = self.bot.get_channel(int(args_list[0]))
            if not channel:
                try:
                    channel = await self.bot.fetch_channel(int(args_list[0]))
                except:
                    pass
            if not channel:
                channel = ctx.channel
                args_list.insert(0, channel)
        else:
            args_list.insert(0, channel)

        embed = disnake.Embed()
        view = disnake.ui.View(timeout=None)

        async def add_button(entry: str):
            args_splitted = await self.get_args(entry)
            style = args_splitted[0]
            label = args_splitted[1]
            disabled = args_splitted[2]
            custom_id = args_splitted[3]
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
                error_msg = "$sendMessage: #addButton: Style incorrect type\n\nPlease, select secondary/success/danger/primary or link type."
                if self.handler.debug_console:
                    raise ValueError(error_msg)
                else:
                    await ctx.channel.send(error_msg)
                    return True

            view.add_item(disnake.ui.Button(style=style, label=label, disabled=disabled.lower() == "true", custom_id=custom_id, url=url, emoji=emoji, row=row))

        async def add_menu(entry: str):
            args_splitted = await self.get_args(await self.is_have_functions(entry, ctx))
            options = []

            async def exec_option(option: str):
                args = await self.get_args(await self.is_have_functions(option, ctx))
                label = args[0]
                value = args[1]
                description = args[2] if len(args) > 2 and len(args[2]) != 0 else None
                emoji = args[3] if len(args) > 3 and len(args[3]) != 0 else None
                default = args[4].lower() == "true" if len(args) > 4 and len(args[4]) != 0 else False
                nonlocal options
                options.append(disnake.SelectOption(label=label, value=value, description=description, emoji=emoji, default=default))

            await self.exec_tags(args_splitted, {"#addoption": exec_option})

            if len(args_splitted) < 2:
                error_msg = "$sendMessage: #addMenu: Placeholder and/or customID does not set.\n\nPlease, provide it."
                if self.handler.debug_console:
                    raise ValueError(error_msg)
                else:
                    await ctx.channel.send(error_msg)
                    return True

            placeholder = args_splitted[0]
            custom_id = args_splitted[1]
            min_values = 1
            if len(args_splitted) > 2 and len(args_splitted[2]) != 0:
                if not args_splitted[2].isdigit():
                    error_msg = "$sendMessage: #addMenu: Min. values argument incorrect type.\n\nPlease, check if you provide integer."
                    if self.handler.debug_console:
                        raise ValueError(error_msg)
                    else:
                        await ctx.channel.send(error_msg)
                        return True
                min_values = int(args_splitted[2])
            max_values = 1
            if len(args_splitted) > 3 and len(args_splitted[3]) != 0:
                if not args_splitted[3].isdigit():
                    error_msg = "$sendMessage: #addMenu: Max. values argument incorrect type.\n\nPlease, check if you provide integer."
                    if self.handler.debug_console:
                        raise ValueError(error_msg)
                    else:
                        await ctx.channel.send(error_msg)
                        return True
                if int(args_splitted[3]) < min_values:
                    error_msg = "$sendMessage: #addMenu: Max. values argument must be grather or equals than min. value.\n\nPlease, set correct value."
                    if self.handler.debug_console:
                        raise ValueError(error_msg)
                    else:
                        await ctx.channel.send(error_msg)
                        return True

                max_values = int(args_splitted[3])
            disabled = False
            if len(args_splitted) > 4 and len(args_splitted[4]) != 0:
                if args_splitted[4].lower() not in ["true", "false"]:
                    error_msg = "$sendMessage: #addMenu: Incorrect value of disabled argument.\n\nPlease, check if yout provide true/false value."
                    if self.handler.debug_console:
                        raise ValueError(error_msg)
                    else:
                        await ctx.channel.send(error_msg)
                        return True

                disabled = args_splitted[4].lower() == "true"

            row = int(args_splitted[5]) if len(args_splitted[5]) != 0 else None

            class NewMenu(disnake.ui.StringSelect):
                def __init__(self):
                    super().__init__(
                        custom_id=custom_id,
                        placeholder=placeholder,
                        min_values=min_values,
                        max_values=max_values,
                        options=options,
                        disabled=disabled,
                        row=row
                    )

            view.add_item(NewMenu())

        async def add_field(entry: str):
            args_splitted = await self.get_args(entry)
            if len(args_splitted) < 2:
                error_msg = "$sendMessage: #addField: Name and value of field are required."
                if self.handler.debug_console:
                    raise ValueError(error_msg)
                else:
                    await ctx.channel.send(error_msg)
                    return True

            inline = False
            if len(args_splitted) > 2:
                inline = args_splitted[2].lower() == "true"
            embed.add_field(args_splitted[0], args_splitted[1], inline=inline)

        isAddReaction = False
        reactions = []
        async def add_reaction(entry: str):
            nonlocal isAddReaction
            isAddReaction = True
            reactions.append(entry)

        is_reply = None
        async def reply_to(entry: str):
            args_splitted = await self.get_args(entry)
            if len(args_splitted) > 2:
                error_msg = "$sendMessage: #reply: Too many args provided."
                if self.handler.debug_console:
                    raise ValueError(error_msg)
                else:
                    await ctx.channel.send(error_msg)
                    return True

            channel = ctx.channel
            if args_list[0].isdigit() and len(args_list) > 2:
                channel = self.bot.get_channel(int(args_list[0]))
                if not channel:
                    channel = await self.bot.fetch_channel(int(args_list[0]))
                if not channel:
                    channel = ctx.channel
                    args_list.insert(0, channel)
            else:
                args_list.insert(0, channel)

            message = None
            error_msg = f"$sendMessage: #reply: Cannot find message \"{args_list[1]}\""
            try:
                message = self.bot.get_message(int(args_list[1]))
                if not message:
                    message = await channel.fetch_message(int(args_list[1]))
                if not message:
                    if self.handler.debug_console:
                        raise SyntaxError(error_msg)
                    else:
                        await ctx.channel.send(error_msg)
                        return True
            except:
                if self.handler.debug_console:
                    raise SyntaxError(error_msg)
                else:
                    await ctx.channel.send(error_msg)
                    return True

            nonlocal is_reply
            is_reply = message

        is_delete = None
        async def delete_in(entry: str):
            args_splitted = await self.get_args(entry)
            if len(args_splitted) > 2 or len(args_splitted) == 0:
                error_msg = "$sendMessage: #deleteIn: Too many args provided."
                if self.handler.debug_console:
                    raise ValueError(error_msg)
                else:
                    await ctx.channel.send(error_msg)
                    return True

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
            nonlocal is_delete
            is_delete = int(args_list[0]) * {'s': 1, 'm': 60, 'h': 60*60, 'd': 60*60*24}[args_list[1]]

        tag_funcs = {
            "#addfield": add_field,
            "#addbutton": add_button,
            "#addmenu": add_menu,
            "#addreaction": add_reaction,
            "#reply": reply_to,
            "#deletein": delete_in 
            }
        await self.exec_tags(args_list, tag_funcs)
        content = None
        if len(args_list) > 1 and len(args_list[1]) > 0:
            content = args_list[1]
        if len(args_list) > 2 and len(args_list[2]) > 0:
            embed.title = args_list[2]
        if len(args_list) > 3 and len(args_list[3]) > 0:
            embed.description = args_list[3]
        if len(args_list) > 4 and len(args_list[4]) > 0:
            icon_url = None
            if len(args_list) > 5 and len(args_list[5]) > 0:
                icon_url = args_list[5]
            embed.set_footer(text=args_list[4], icon_url=icon_url)
        if len(args_list) > 6 and len(args_list[6]) > 0:
            embed.color = disnake.Colour(int("0x"+(args_list[6].replace("#", "0x").replace("0x", "")), 16))
        if len(args_list) > 7 and len(args_list[7]) > 0:
            embed.set_thumbnail(args_list[7])
        if len(args_list) > 8 and len(args_list[8]) > 0:
            embed.set_image(args_list[8])
        if len(args_list) > 9 and len(args_list[9]) > 0:
            url = None
            if len(args_list) > 10 and len(args_list[10]) > 0:
                url = args_list[10]
            icon_url = None
            if len(args_list) > 11 and len(args_list[11]) > 0:
                icon_url = args_list[11]
            embed.set_author(name=args_list[9], url=url, icon_url=icon_url)
        return_id = False
        if len(args_list) > 12 and len(args_list[12]) > 0:
            return_id = True

        if len(embed.to_dict()) < 2:
            embed = None
        message = None
        try:
            if is_reply:
                message = await is_reply.reply(content=content, embed=embed, view=view)
            else:
                if isinstance(ctx, disnake.AppCmdInter) and return_id:
                    message = await disnake.AppCmdInter.send(content=content, embed=embed, view=view, ephemeral=True, delete_after=is_delete)
                else:
                    message = await channel.send(content=content, embed=embed, view=view, delete_after=is_delete)
        except disnake.errors.HTTPException as e:
            if self.handler.debug_console:
                print(f"$sendMessage: {e.text}")
            else:
                await ctx.channel.send(f"$sendMessage: {e.text}")
            return True
        if isAddReaction:
            for i in reactions:
                await message.add_reaction(i)
        if return_id and not isinstance(ctx, disnake.AppCmdInter):
            return str(message.id)

def setup(handler):
    return Functions(handler)
