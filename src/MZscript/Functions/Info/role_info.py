import disnake

from ...functions_handler import FunctionsHandler


class RoleInfo(FunctionsHandler):
    def __init__(self, handler):
        super().__init__()
        self.handler = handler
        self.bot = handler.client.bot

    async def func_roleinfo(self, ctx: disnake.Message, args: str):
        """
        `$userInfo[(guild;user);param]`
        ### Example:
        `$userInfo[id]`
        ### Example 2:
        `$userInfo[700061502089986139;name]`
        """
        args_list = await self.get_args(await self.is_have_functions(args, ctx), ctx)
        if len(args_list) > 3 or len(args_list) == 0:
            raise ValueError("$roleInfo: Too many or no args provided")

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
                raise SyntaxError(f"$roleInfo: Cannot find guild \"{args_list[0]}\"")
        else:
            args_list.insert(0, guild)

        role = None
        if args_list[1].isdigit():
            try:
                role = guild.get_role(int(args_list[1]))
                if not role:
                    role = await guild.fetch_role(int(args_list[1]))
                if not role:
                    raise SyntaxError(f"$roleInfo: Cannot find role \"{args_list[1]}\"")
            except Exception as e:
                print(e)
                raise SyntaxError(f"$roleInfo: Cannot find role \"{args_list[1]}\"")
        else:
            raise SyntaxError(f"$roleInfo: Cannot find role \"{args_list[1]}\"")

        params = {
            "color": role.color,
            "created": int(role.created_at.timestamp()),
            "emoji": role.emoji,
            "guild": role.guild.id,
            "hoist": str(role.hoist).lower(),
            "managed": str(role.managed).lower(),
            "mention": str(role.mentionable).lower(),
            "name": role.name,
            "position": role.position,
            "tags": role.tags
        }

        return str(params[args_list[2]])

def setup(handler):
    return RoleInfo(handler)