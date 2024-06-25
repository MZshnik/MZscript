import disnake

from src.MZscript.functions_handler import FunctionsHandler


class Functions(FunctionsHandler):
    def __init__(self, handler):
        super().__init__()
        self.client = handler.client
        self.bot = handler.client.bot

    async def func_var(self, ctx, args: str):
        """
        `$var[name;time]`
        #### Example:
        `$var[lastuser]`
        #### Example 2:
        `$var[owner;global]`
        #### Example 3:
        `$var[set;owner;$userInfo[id]]`
        #### Example 4:
        `$var[del;owner;$userInfo[id];global]`
        """
        args_list = await self.get_args(await self.is_have_functions(args))
        time = "global" if args_list[-1] == "global" else "temp"
        result = None
        if args_list[0] not in ["get", "set", "del"]:
            args_list.insert(0, "get")
        if args_list[0] == "get":
            result = await self.database.get_json_var(args_list[1], time)
        elif args_list[0] == "set":
            result = await self.database.set_json_var(args_list[1], args_list[2], time)
        elif args_list[0] == "del":
            result = await self.database.del_json_var(args_list[1], time)
        if result:
            return result
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

def setup(handler):
    return Functions(handler)