import disnake

from ...functions_handler import FunctionsHandler


class ChannelInfo(FunctionsHandler):
    def __init__(self, handler):
        super().__init__()
        self.handler = handler
        self.bot = handler.client.bot

    async def func_channelinfo(self, ctx: disnake.message.Message, args: str):
        """
        `$channelInfo[(channel);param]`
        #### Example:
        `$channelInfo[id]`
        #### Example 2:
        `$channelInfo[951193622429184000;name]`
        """
        args_list = await self.get_args(await self.is_have_functions(args, ctx), ctx)
        if len(args_list) > 2 or len(args_list) == 0:
            raise ValueError("$channelInfo: Too many or no args provided")

        channel = ctx.channel
        if args_list[0].isdigit():
            try:
                channel = self.bot.get_channel(int(await self.is_have_functions(args_list[0], ctx)))
            except Exception as e:
                print(e)
                raise SyntaxError(f"$channelInfo: Cannot find channel \"{args_list[0]}\"")
        else:
            if len(args_list) == 1:
                args_list.insert(0, channel)
            else:
                id = int(args_list[0].replace("<#", "").replace(">", ""))
                channel = await self.bot.fetch_channel(id)

        params = {
            "category": channel.category.id,
            "created": int(channel.created_at.timestamp()),
            "guild": channel.guild.id,
            "name": channel.name,
            "id": channel.id,
            "type": channel.type,
            "position": channel.position,
            "last_message": channel.last_message.id if channel.type == disnake.ChannelType.text else "",
            "nsfw": str(channel.nsfw).lower() if channel.type == disnake.ChannelType.text else "",
            "slowmode_delay": channel.slowmode_delay if channel.type == disnake.ChannelType.text else "",
            "thread_slowmode": channel.default_thread_slowmode_delay if channel.type == disnake.ChannelType.text else "",
            "auto_archive_duration": channel.default_auto_archive_duration if channel.type == disnake.ChannelType.text else "",
            "topic": channel.topic if channel.type == disnake.ChannelType.text else "",
            "bitrate": channel.bitrate if channel.type == disnake.ChannelType.voice else "",
            "user_limit": channel.user_limit if channel.type == disnake.ChannelType.voice else "",
            "region": channel.rtc_region if channel.type == disnake.ChannelType.voice else ""
        }

        return str(params[args_list[1]])

def setup(handler):
    return ChannelInfo(handler)