import disnake

from ...functions_handler import FunctionsHandler


class UserInfo(FunctionsHandler):
    def __init__(self, handler):
        super().__init__()
        self.handler = handler
        self.bot = handler.client.bot

    async def func_userinfo(self, ctx: disnake.message.Message, args: str):
        """
        `$userInfo[(user);param]`
        #### Example:
        `$userInfo[id]`
        #### Example 2:
        `$userInfo[700061502089986139;name]`
        """
        args_list = await self.get_args(await self.is_have_functions(args, ctx), ctx)
        if len(args_list) > 2 or len(args_list) == 0:
            raise ValueError("$userInfo: Too many or no args provided")

        user = ctx.author
        if args_list[0].isdigit() and len(args_list) > 1:
            try:
                user = await self.bot.get_or_fetch_user(int(await self.is_have_functions(args_list[0], ctx)))
                if not user:
                    raise SyntaxError(f"$userInfo: Cannot find user \"{args_list[0]}\"")
            except Exception as e:
                print(e)
                raise SyntaxError(f"$userInfo: Cannot find user \"{args_list[0]}\"")
        else:
            args_list.insert(0, user)

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
            "system": user.system
        }

        if args_list[1] == "dm":
            if not user.dm_channel:
                user.create_dm()
            return str(params[args_list[1]].id)
        return str(params[args_list[1]])

def setup(handler):
    return UserInfo(handler)