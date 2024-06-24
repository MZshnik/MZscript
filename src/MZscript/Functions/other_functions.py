import disnake

from MZscript.functions_handler import FunctionsHandler


class Functions(FunctionsHandler):
    def __init__(self, handler):
        super().__init__()
        self.client = handler.client
        self.bot = handler.client.bot

    async def func_message(self, ctx: disnake.message.Message, args: str = ""):
        if len(args) == 0:
            return ctx.content
        return ctx.content.split(" ")[int(args)]

    async def func_addreaction(self, ctx, args: str):
        args_list = await self.get_args(await self.is_have_functions(args, ctx))

        guild = ctx.guild
        if args_list[0].isdigit() and len(args_list) > 2:
            try:
                if not self.bot.get_channel(int(args_list[0])):
                    guild = self.bot.get_guild(int(args_list[0]))
                args_list.insert(0, guild)
            except:
                raise SyntaxError(f"$addReaction")
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

    async def func_userinfo(self, ctx: disnake.message.Message, args: str):
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
                raise SyntaxError(f"$sendMessage: Cannot find channel \"{args_list[0]}\"")
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