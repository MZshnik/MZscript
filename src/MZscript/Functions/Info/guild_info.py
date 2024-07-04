import disnake

from ...functions_handler import FunctionsHandler


class GuildInfo(FunctionsHandler):
    def __init__(self, handler):
        super().__init__()
        self.handler = handler
        self.bot = handler.client.bot

    async def func_guildinfo(self, ctx: disnake.Message, args: str):
        """
        `$guildInfo[(guild);param]`
        ### Example:
        `$guildInfo[name]`
        ### Example 2:
        `$guildInfo[796504104565211187;icon]`
        """
        args_list = await self.get_args(await self.is_have_functions(args, ctx), ctx)
        if len(args_list) > 2 or len(args_list) == 0:
            raise ValueError("$guildInfo: Too many or no args provided")

        guild = ctx.guild
        if args_list[0].isdigit() and len(args_list) > 1:
            try:
                guild = self.bot.get_guild(int(args_list[0]))
                if not guild:
                    guild = await self.bot.fetch_guild(int(args_list[0]))
                if not guild:
                    raise SyntaxError(f"$guildInfo: Cannot find guild \"{args_list[0]}\"")
            except Exception as e:
                print(e)
                raise SyntaxError(f"$guildInfo: Cannot find guild \"{args_list[0]}\"")
        else:
            args_list.insert(0, guild)

        params = {
            "afk_channel": "",
            "banner": guild.banner,
            "categories": guild.categories,
            "channels": guild.channels,
            "created": int(guild.created_at.timestamp()),
            "description": guild.description,
            "emoji_limit": guild.emoji_limit,
            "emojis": guild.emojis,
            "forums": guild.forum_channels,
            "icon": guild.icon,
            "id": guild.id,
            "members": guild.member_count,
            "mfa": guild.mfa_level,
            "name": guild.name,
            "ownerid": guild.owner.id,
            "boost_progress_bar": guild.premium_progress_bar_enabled,
            "boost_role": guild.premium_subscriber_role.id,
            "boosters": guild.premium_subscribers,
            "boosts": guild.premium_subscription_count,
            "boost_level": guild.premium_tier,
            "rules_channel": guild.rules_channel.id,
            "safety_channel": guild.safety_alerts_channel.id,
            "stages": guild.stage_channels,
            "system_channel": guild.system_channel.id,
            "sticker_limit": guild.sticker_limit,
            "stickers": guild.stickers,
            "verification_level": guild.verification_level,
            "widget_channel": guild.widget_channel_id,
            "widget": guild.widget_enabled
        }
        if guild.afk_channel:
            params["afk_channel"] = guild.afk_channel.id

        return str(params[args_list[1]])

def setup(handler):
    return GuildInfo(handler)