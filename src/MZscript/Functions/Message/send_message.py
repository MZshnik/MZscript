import disnake

from ...functions_handler import FunctionsHandler


class Functions(FunctionsHandler):
    def __init__(self, handler):
        super().__init__()
        self.handler = handler
        self.bot = handler.client.bot

    async def func_sendmessage(self, ctx: disnake.Message, args: str):
        """
        `$sendMessage[(channel;content;title;description;footer;footer icon;color;thumbnail;image;author;author url;author icon)]`
        #### Example:
        `$sendMessage[hello]`
        #### Example 2:
        `$sendMessage[$userInfo[dm];;Welcome!;Welcome to new guild "$guildInfo[name]";;;0058CF]`
        """
        args_list = await self.get_args(await self.is_have_functions(args, ctx))
        if len(args_list) < 1:
            error_msg = f"$sendMessage: Needs 1 arguments, but only {len(args_list)} provided: \"{args}\""
            if self.handler.debug_console:
                raise ValueError(error_msg)
            else:
                await ctx.channel.send(error_msg)
                return True

        channel = ctx.channel
        if args_list[0].isdigit() and len(args_list) > 1:
            try:
                channel = self.bot.get_channel(int(args_list[0]))
                if not channel:
                    channel = await self.bot.fetch_channel(int(args_list[0]))
                if not channel:
                    channel = ctx.channel
                    args_list.insert(0, channel)
            except Exception as e:
                print(e)
                raise SyntaxError(f"$sendMessage: Cannot find channel \"{args_list[0]}\"")
        else:
            args_list.insert(0, channel)
        embed = disnake.Embed()
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
            args_splited = await self.get_args(entry, ctx)
            if len(args_splited) < 2:
                raise ValueError("$sendMessage: #addField: Name and value of field are required.")
            inline = False
            if len(args_splited) > 2:
                inline = args_splited[2].lower() == "true"
            embed.add_field(args_splited[0], args_splited[1], inline=inline)

        isAddReaction = False
        reactions = []
        async def add_reaction(entry: str):
            nonlocal isAddReaction
            isAddReaction = True
            reactions.append(entry)

        tag_funcs = {
            "#addfield": add_field,
            "#addbutton": add_button,
            "#addreaction": add_reaction
            }
        counter = len(args_list)
        for i in args_list.copy()[::-1]:
            counter -= 1
            for tag in tag_funcs.keys():
                if str(i).lower().startswith(tag.lower()):
                    await tag_funcs[tag](i[len(tag)+1:-1])
                    args_list.pop(counter)
        content = None
        if len(args_list) > 1 and len(args_list[1]) > 0:
            content = args_list[1]
        if len(args_list) > 2 and len(args_list[2]) > 0:
            embed.title = args_list[2]
        if len(args_list) > 3 and len(args_list[3]) > 0:
            embed.description = args_list[3]
            if not embed.description:
                raise SyntaxError(f"$sendMessage: Cannot send embed without description: {args}")
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

        if not embed.description:
            embed = None
        message = await channel.send(content=content, embed=embed, view=view)
        if isAddReaction:
            for i in reactions:
                await message.add_reaction(i)

def setup(handler):
    return Functions(handler)
