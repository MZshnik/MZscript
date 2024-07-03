import disnake

from ...functions_handler import FunctionsHandler


class Functions(FunctionsHandler):
    def __init__(self, handler):
        super().__init__()
        self.handler = handler
        self.bot = handler.client.bot

    async def func_var(self, ctx, args: str):
        """
        `$var[(mode);name;(newvalue);time]`
        ### Example:
        `$var[lastuser]`
        ### Example 2:
        `$var[owner;global]`
        ### Example 3:
        `$var[set;owner;$userInfo[id]]`
        ### Example 4:
        `$var[del;owner;$userInfo[id];global]`
        """
        args_list = await self.get_args(await self.is_have_functions(args))
        time = "global" if args_list[-1] == "global" else "temp"
        result = None
        if args_list[0] not in ["get", "set", "del"]:
            args_list.insert(0, "get")
        if args_list[0] == "get":
            result = await self.handler.database.get_json_var(args_list[1], time)
        elif args_list[0] == "set":
            result = await self.handler.database.set_json_var(args_list[1], args_list[2], time)
        elif args_list[0] == "del":
            result = await self.handler.database.del_json_var(args_list[1], time)
        if result:
            return result
        return ""

    async def func_getvar(self, ctx, args: str):
        """
        `$getVar[name]`
        """
        result = await self.handler.database.get_global_var(await self.is_have_functions(args, ctx))
        if result:
            return result
        elif self.handler.db_warns:
            print(f"WARNING: Value for global var \"{args}\" not provided (returning empty string)")
        return ""

    async def func_setvar(self, ctx, args: str):
        """
        `$setVar[name;value]`
        """
        args_list = await self.get_args(await self.is_have_functions(args, ctx))
        if len(args_list) != 2:
            error_msg = f"$setVar: Too many or no args provided"
            if self.handler.debug_console:
                raise ValueError(error_msg)
            await ctx.channel.send(error_msg)
            return True
        await self.handler.database.set_global_var(args_list[0], args_list[1])

    async def func_delvar(self, ctx, args: str):
        """
        `$delVar[name]`
        """
        args_list = await self.get_args(await self.is_have_functions(args, ctx))
        if len(args_list) != 1:
            error_msg = "$delVar: Too many or no args provided"
            if self.handler.debug_console:
                raise ValueError(error_msg)
            await ctx.channel.send(error_msg)
            return True
        await self.handler.database.set_global_var(args_list[0])

    async def func_getmembervar(self, ctx, args: str):
        """
        `$getMemberVar[name;(user;guild)]`
        """
        args_list = await self.get_args(await self.is_have_functions(args, ctx))
        if len(args_list) < 1 or len(args_list) > 3:
            error_msg = f"$getMemberVar: Too many or no args provided"
            if self.handler.debug_console:
                raise ValueError(error_msg)
            await ctx.channel.send(error_msg)
            return True
        if len(args_list) == 1:
            args_list.append(ctx.author.id)
        if len(args_list) == 2:
            args_list.append(ctx.guild.id)
        result = await self.handler.database.get_value_from_member(args_list[2], args_list[1], args_list[0])
        if result:
            return result
        elif self.handler.db_warns:
            print(f"WARNING: Value for member var \"{args_list[0]}\" not provided (returning empty string)")
        return ""

    async def func_setmembervar(self, ctx, args: str):
        """
        `$setMemberVar[name;value;(user;guild)]`
        """
        args_list = await self.get_args(await self.is_have_functions(args, ctx))
        if len(args_list) < 2 or len(args_list) > 4:
            error_msg = "$setMemberVar: Too many or no args provided"
            if self.handler.debug_console:
                raise ValueError(error_msg)
            await ctx.channel.send(error_msg)
            return True
        if len(args_list) == 2:
            args_list.append(ctx.author.id)
        if len(args_list) == 3:
            args_list.append(ctx.guild.id)
        await self.handler.database.set_value_of_member(args_list[3], args_list[2], args_list[0], args_list[1])

    async def func_delmembervar(self, ctx, args: str):
        """
        `$delMemberVar[name;(user;guild)]`
        """
        args_list = await self.get_args(await self.is_have_functions(args, ctx))
        if len(args_list) < 1:
            error_msg = f"$delMemberVar: Too many or no args provided"
            if self.handler.debug_console:
                raise ValueError(error_msg)
            await ctx.channel.send(error_msg)
            return True
        if len(args_list) == 1:
            args_list.append(ctx.author.id)
        if len(args_list) == 2:
            args_list.append(ctx.guild.id)
        await self.handler.database.del_value_of_member(args_list[2], args_list[1], args_list[0])

    async def func_getguildvar(self, ctx, args: str):
        """
        `$getGuildVar[name;(guild)]`
        """
        args_list = await self.get_args(await self.is_have_functions(args, ctx))
        if len(args_list) < 1:
            error_msg = f"$getGuildVar: Too many or no args provided"
            if self.handler.debug_console:
                raise ValueError(error_msg)
            await ctx.channel.send(error_msg)
            return True
        if len(args_list) == 1:
            args_list.append(ctx.guild.id)
        result = await self.handler.database.get_value_from_guild(args_list[1], args_list[0])
        if result:
            return result
        elif self.handler.db_warns:
            print(f"WARNING: Value for guild var \"{args_list[0]}\" not provided (returning empty string)")
        return ""

    async def func_setguildvar(self, ctx, args: str):
        """
        `$setGuildVar[name;(guild)]`
        """
        args_list = await self.get_args(await self.is_have_functions(args, ctx))
        if len(args_list) < 2:
            error_msg = f"$setGuildVar: Too many or no args provided"
            if self.handler.debug_console:
                raise ValueError(error_msg)
            await ctx.channel.send(error_msg)
            return True
        if len(args_list) == 2:
            args_list.append(ctx.guild.id)
        await self.handler.database.set_value_of_guild(args_list[2], args_list[0], args_list[1])

    async def func_delguildvar(self, ctx, args: str):
        """
        `$delGuildVar[name;(guild)]`
        """
        args_list = await self.get_args(await self.is_have_functions(args, ctx))
        if len(args_list) < 1:
            error_msg = f"$delGuildVar: Too many or no args provided"
            if self.handler.debug_console:
                raise ValueError(error_msg)
            await ctx.channel.send(error_msg)
            return True
        if len(args_list) == 1:
            args_list.append(ctx.guild.id)
        await self.handler.database.del_value_of_guild(args_list[1], args_list[0])

    async def func_getuservar(self, ctx, args: str):
        """
        `$getUserVar[name;(user)]`
        """
        args_list = await self.get_args(await self.is_have_functions(args, ctx))
        if len(args_list) < 1:
            error_msg = f"$getUserVar: Too many or no args provided"
            if self.handler.debug_console:
                raise ValueError(error_msg)
            await ctx.channel.send(error_msg)
            return True
        if len(args_list) == 1:
            args_list.append(ctx.author.id)
        result = await self.handler.database.get_value_from_user(args_list[1], args_list[0])
        if result:
            return result
        elif self.handler.db_warns:
            print(f"WARNING: Value for user var \"{args_list[0]}\" not provided (returning empty string)")
        return ""

    async def func_setuservar(self, ctx, args: str):
        """
        `$setUserVar[name;value;(user)]`
        """
        args_list = await self.get_args(await self.is_have_functions(args, ctx))
        if len(args_list) < 2:
            error_msg = f"$setUserVar: Too many or no args provided"
            if self.handler.debug_console:
                raise ValueError(error_msg)
            await ctx.channel.send(error_msg)
            return True
        if len(args_list) == 2:
            args_list.append(ctx.author.id)
        await self.handler.database.set_value_of_user(args_list[2], args_list[0], args_list[1])

    async def func_deluservar(self, ctx, args: str):
        """
        `$delUserVar[name;(user)]`
        """
        args_list = await self.get_args(await self.is_have_functions(args, ctx))
        if len(args_list) < 1:
            error_msg = f"$delUserVar: Too many or no args provided"
            if self.handler.debug_console:
                raise ValueError(error_msg)
            await ctx.channel.send(error_msg)
            return True
        if len(args_list) == 1:
            args_list.append(ctx.author.id)
        await self.handler.database.del_value_of_user(args_list[1], args_list[0])

def setup(handler):
    return Functions(handler)