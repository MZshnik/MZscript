import disnake

from MZscript.functions_handler import FunctionsHandler


class Functions(FunctionsHandler):
    def __init__(self, handler):
        super().__init__()
        self.client = handler.client
        self.bot = handler.client.bot

    async def func_message(self, ctx: disnake.message.Message, args: str = ""):
        """
        `$message[arg number]`
        #### Example:
        `$message`
        #### Example 2:
        `$message[0]`
        """
        if len(args) == 0:
            return ctx.content
        return ctx.content.split(" ")[int(args)]

    async def func_addreaction(self, ctx: disnake.message.Message, args: str):
        """
        `$addReaction[(channel);(message);emoji]`
        #### Example:
        `$addReaction[🚀]`
        #### Example 2:
        `$addReaction[1254895980424466462;😎]`
        """
        args_list = await self.get_args(await self.is_have_functions(args, ctx))

        guild = ctx.guild
        if args_list[0].isdigit() and len(args_list) > 2:
            try:
                if not self.bot.get_channel(int(args_list[0])):
                    guild = self.bot.get_guild(int(args_list[0]))
                args_list.insert(0, guild)
            except Exception as e:
                print(e)
                raise SyntaxError(f"$addReaction: Cannot find guild \"{args_list[0]}\"")
        else:
            args_list.insert(0, guild)

        channel = disnake.utils.get(ctx.guild.text_channels, id=ctx.channel.id)
        if len(args_list) > 3 and len(args_list[1]) > 0:
            channel = disnake.utils.get(ctx.guild.text_channels, id=int(args_list[1]))
            args_list[1] = channel
        else:
            args_list.insert(1, channel)
        message = await channel.fetch_message(int(args_list[2]))

        await message.add_reaction(emoji=args_list[3])

    async def func_channelinfo(self, ctx: disnake.message.Message, args: str):
        """
        `$channelInfo[(channel);param]`
        #### Example:
        `$channelInfo[name]`
        #### Example 2:
        `$channelInfo[951193622429184000;topic]`\n
        All channel params:
        - name
        - guild (if exists)
        - id
        - category
        - topic
        - position
        - last_message
        - slowmode
        - thread_slowmode
        - nsfw
        - auto_archive_duration
        """
        args = await self.is_have_functions(args, ctx)
        args_list = await self.get_args(args, ctx)
        if len(args_list) > 2 or len(args_list) == 0:
            raise ValueError("$channelInfo: To many or no args provided")
        channel = ctx.channel
        if args_list[0].isdigit():
            try:
                channel = self.bot.get_channel(int(await self.is_have_functions(args_list[0], ctx)))
            except Exception as e:
                print(e)
                raise SyntaxError(f"$channelInfo: Cannot find channel \"{args_list[0]}\"")
        else:
            args_list.insert(0, channel)
        params = {
            "name": channel.name,
            "guild": channel.guild.id,
            "id": channel.id,
            "category": channel.category_id,
            "topic": channel.topic,
            "position": channel.position,
            "last_message": channel.last_message_id,
            "slowmode": channel.slowmode_delay,
            "thread_slowmode": channel.default_thread_slowmode_delay,
            "nsfw": str(channel.nsfw).lower(),
            "auto_archive_duration": channel.default_auto_archive_duration
            }
        return str(params[args_list[1]])

    async def func_userinfo(self, ctx: disnake.message.Message, args: str):
        """
        `$userInfo[(user);param]`
        #### Example:
        `$userInfo[name]`
        #### Example 2:
        `$userInfo[700061502089986139;avatar]`\n
        All channel params:
        - name
        - id
        - avatar
        - dm
        - created
        - global
        - bot
        - system
        """
        args = await self.is_have_functions(args, ctx)
        args_list = await self.get_args(args, ctx)
        if len(args_list) > 2 or len(args_list) == 0:
            raise ValueError("$userInfo: To many or no args provided")
        user = ctx.author
        if args_list[0].isdigit():
            try:
                user = self.bot.get_user(int(await self.is_have_functions(args_list[0], ctx)))
            except Exception as e:
                print(e)
                raise SyntaxError(f"$userInfo: Cannot find user \"{args_list[0]}\"")
        else:
            args_list.insert(0, user)
        params = {
            "name": user.name,
            "id": user.id,
            "avatar": user.avatar,
            "dm": user.dm_channel,
            "created": int(user.created_at.timestamp()),
            "global": user.global_name,
            "bot": user.bot,
            "system": user.system
            }
        return str(params[args_list[1]])

    async def func_text(self, ctx: disnake.message.Message, args: str):
        """
        `$text[text]`
        #### Example:
        `$text[$sendMessage[this function like text]]`
        """
        return args

    async def func_kick(self, ctx, args: str = None):
        args_list = await self.get_args(await self.is_have_functions(args, ctx))

        guild = ctx.guild
        if args_list[0].isdigit() and len(args_list) > 1:
            try:
                if not self.bot.get_user(int(args_list[0])):
                    guild = self.bot.get_guild(int(args_list[0]))
            except Exception as e:
                print(e)
                raise SyntaxError(f"$kick: Cannot find guild \"{args_list[0]}\"")
        args_list.insert(0, guild)

        reason = None
        if len(args_list) > 2 and len(args_list[2]) > 0:
            reason = args_list[2]

        await guild.kick(user=await guild.fetch_member(args_list[1]), reason=reason)

    async def func_customid(self, ctx: disnake.MessageInteraction, args: str = None):
        return ctx.component.custom_id

    async def func_defer(self, ctx: disnake.MessageInteraction, args: str = None):
        await ctx.response.defer()
        return ""

    async def func_updatecommands(self, ctx, args: str = None):
        await self.client.update_commands()

    async def func_calculate(self, ctx, args: str):
        args = await self.is_have_functions(args, ctx)
        from ast import Name, parse, walk

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

def setup(handler):
    return Functions(handler)