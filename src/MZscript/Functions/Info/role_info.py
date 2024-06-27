import disnake

from ...functions_handler import FunctionsHandler


class RoleInfo(FunctionsHandler):
    def __init__(self, handler):
        super().__init__()
        self.handler = handler
        self.bot = handler.client.bot

    # [roleid;params]
    async def func_roleinfo(self, ctx: disnake.message.Message, args: str):
        args_list = await self.get_args(await self.is_have_functions(args, ctx), ctx)


        if len(args_list) > 2 or len(args_list) == 0:
            raise ValueError("$roleInfo: To many or no args provided")

        role = ctx.guild.get_role(args_list[0])
        if args_list[0].isdigit():
            try:
                role = ctx.guild.get_role(int(await self.is_have_functions(args_list[0], ctx)))
            except Exception as e:
                print(e)
                raise SyntaxError(f"$roleInfo: Cannot find role \"{args_list[0]}\"")
        else:
            if len(args_list) == 1:
                args_list.insert(0, role)
            else:
                id = int(args_list[0].replace("<@&", "").replace(">", ""))
                role = ctx.guild.get_role(id)
                
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

        return str(params[args_list[1]])

def setup(handler):
    return RoleInfo(handler)