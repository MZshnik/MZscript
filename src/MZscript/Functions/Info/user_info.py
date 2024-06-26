import disnake

from MZscript.functions_handler import FunctionsHandler

class UserInfo(FunctionsHandler):
    def __init__(self, handler):
        super().__init__()
        self.client = handler.client
        self.bot = handler.client.bot

    # [userid?;params]
    async def func_userinfo(self, ctx: disnake.message.Message, args: str):
        args = await self.is_have_functions(args, ctx)
        args_list = await self.get_args(args, ctx)

        # if len(args_list[0]) == "":
        #     raise ValueError("$userInfo: User not provided")

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
            if len(args_list) == 1:
                args_list.insert(0, user)
            else:
                id = int(args_list[0].replace("<@", "").replace(">", ""))
                user = await self.bot.fetch_user(id)
                
        params = {
            "avatar": user.avatar,
            "banner": user.banner,
            "bot": user.bot,
            "created": int(user.created_at.timestamp()),
            "name": user.name,
            "display_name": user.display_name,
            "global_name": user.global_name,
            "id": user.id,
            "system": user.system
        }

        return str(params[args_list[1]])

def setup(handler):
    return UserInfo(handler)