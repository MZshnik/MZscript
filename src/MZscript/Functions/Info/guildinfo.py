import disnake

from src.MZscript.functions_handler import FunctionsHandler

class GuildInfo(FunctionsHandler):
    def __init__(self, handler):
        super().__init__()
        self.client = handler.client
        self.bot = handler.client.bot

    # [guildid?;params]
    async def func_guildinfo(self, ctx: disnake.message.Message, args: str):
        args = await self.is_have_functions(args, ctx)
        args_list = await self.get_args(args, ctx)

        if len(args_list) > 2 or len(args_list) == 0:
            raise ValueError('$guildInfo: To many or no args provided')

        guild = ctx.guild
        if args_list[0].isdigit():
            try:
                guild = self.bot.get_guild(int(await self.is_have_functions(args_list[0], ctx)))
            except Exception as e:
                print(e)
                raise SyntaxError(f'$guildInfo: Cannot find guild "{args_list[0]}"')
        else:
            args_list.insert(0, guild)

        params = {
            'afk_channel': guild.afk_channel.id,
            'banner': guild.banner,
            'categories': guild.categories,
            'channels': guild.channels,
            'created': int(guild.created_at.timestamp()),
            'description': guild.description,
            'emoji_limit': guild.emoji_limit,
            'emojis': guild.emojis,
            'forums': guild.forum_channels,
            'icon': guild.icon,
            'id': guild.id,
            'members': guild.member_count,
            'mfa': guild.mfa_level,
            'name': guild.name,
            'ownerid': guild.owner.id,
            'boost_progress_bar': guild.premium_progress_bar_enabled,
            'boost_role': guild.premium_subscriber_role.id,
            'boosters': guild.premium_subscribers,
            'boosts': guild.premium_subscription_count,
            'boost_level': guild.premium_tier,
            'region': guild.region,
            'rules_channel': guild.rules_channel.id,
            'safety_channel': guild.safety_alerts_channel.id,
            'stages': guild.stage_channels,
            'system_channel': guild.system_channel.id,
            'sticker_limit': guild.sticker_limit,
            'stickers': guild.stickers,
            'verification_level': guild.verification_level,
            'widget_channel': guild.widget_channel_id,
            'widget': guild.widget_enabled
        }

        return str(params[args_list[1]])

def setup(handler):
    return GuildInfo(handler)