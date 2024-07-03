import disnake

from ...functions_handler import FunctionsHandler


class UserInfo(FunctionsHandler):
    def __init__(self, handler):
        super().__init__()
        self.handler = handler
        self.bot = handler.client.bot

    async def func_userinfo(self, ctx: disnake.Message, args: str):
        """
        `$userInfo[(guild;user);param]`
        ### Example:
        `$userInfo[id]`
        ### Example 2:
        `$userInfo[700061502089986139;name]`
        """
        args_list = await self.get_args(await self.is_have_functions(args, ctx), ctx)
        if len(args_list) > 3 or len(args_list) == 0:
            raise ValueError("$userInfo: Too many or no args provided")

        guild = ctx.guild
        if args_list[0].isdigit() and len(args_list) > 1:
            try:
                guild = self.bot.get_guild(int(args_list[0]))
                if not guild:
                    guild = await self.bot.fetch_guild(int(args_list[0]))
                if not guild:
                    guild = ctx.guild
                    args_list.insert(0, guild)
            except Exception as e:
                print(e)
                raise SyntaxError(f"$userInfo: Cannot find guild \"{args_list[0]}\"")
        else:
            args_list.insert(0, guild)

        user = ctx.author
        if args_list[1].isdigit() and len(args_list) > 2:
            try:
                user = await guild.get_or_fetch_member(int(args_list[1]))
                if not user:
                    user = await self.bot.get_or_fetch_user(int(args_list[1]))
                if not user:
                    raise SyntaxError(f"$userInfo: Cannot find user \"{args_list[1]}\"")
            except Exception as e:
                print(e)
                raise SyntaxError(f"$userInfo: Cannot find user \"{args_list[1]}\"")
        else:
            args_list.insert(1, user)

        params = {
            "avatar": user.avatar,
            "banner": user.banner,
            "bot": user.bot,
            "created": int(user.created_at.timestamp()),
            "name": user.name,
            "display_name": user.display_name,
            "global_name": user.global_name,
            "id": user.id,
            "dm": user.dm_channel,
            "system": user.system,
            "timeout": "",
            "joined": "",
            "status": ""
        }
        if isinstance(user, disnake.Member):
            if user.current_timeout:
                params["timeout"] = int(user.current_timeout.timestamp())
            params["joined"] = int(user.joined_at.timestamp())
            params["status"] = user.status

        if args_list[1] == "dm":
            if not user.dm_channel:
                user.create_dm()
            return str(params[args_list[2]].id)
        return str(params[args_list[2]])

def setup(handler):
    return UserInfo(handler)