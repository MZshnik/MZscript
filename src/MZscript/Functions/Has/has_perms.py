import disnake

from ...functions_handler import FunctionsHandler


class Functions(FunctionsHandler):
    def __init__(self, handler):
        super().__init__()
        self.handler = handler
        self.bot = handler.client.bot

    async def func_hasperms(self, ctx: disnake.Message, args: str):
        """
        `$hasPerms[(guild;user);perm]`
        """
        print("And how tou")
        args_list = await self.get_args(await self.is_have_functions(args, ctx), ctx)
        if len(args_list) > 2 or len(args_list) == 0:
            raise ValueError("$hasPerms: Too many or no args provided")

        guild = ctx.guild
        if len(args_list) == 2:
            if not args_list[0].isdigit():
                error_msg = f"$hasPerms: Guild id must be number: \"{args_list[0]}\""
                if self.handler.debug_console:
                    raise SyntaxError(error_msg)
                await ctx.channel.send(error_msg)
                return True

            guild = self.bot.get_guild(int(args_list[0]))
            if not guild:
                guild = await self.bot.fetch_guild(int(args_list[0]))
            if not guild:
                error_msg = f"$hasPerms: Cannot find guild \"{args_list[0]}\""
                if self.handler.debug_console:
                    raise SyntaxError(error_msg)
                await ctx.channel.send(error_msg)
                return True
        else:
            args_list.insert(0, guild)

        user = await guild.get_or_fetch_member(int(ctx.author.id))
        if len(args_list) > 1:
            if not args_list[1].isdigit():
                error_msg = f"$hasPerms: User id must be number: \"{args_list[1]}\""
                if self.handler.debug_console:
                    raise SyntaxError(error_msg)
                await ctx.channel.send(error_msg)
                return True

            user = await guild.get_or_fetch_member(int(args_list[1]))
            if not user:
                error_msg = f"$hasPerms: Cannot find member \"{args_list[1]}\""
                if self.handler.debug_console:
                    raise SyntaxError(error_msg)
                await ctx.channel.send(error_msg)
                return True

        perms = {
        	"add_reactions": user.guild_permissions.add_reactions,
            	"admin": user.guild_permissions.administrator,
            	"attach_files": user.guild_permissions.attach_files,
            	"ban_members": user.guild_permissions.ban_members,
            	"change_nickname": user.guild_permissions.change_nickname,
            	"connect": user.guild_permissions.connect,
            	"create_forum_threads": user.guild_permissions.create_forum_threads,
            	"create_instant_invite": user.guild_permissions.create_instant_invite,
            	"create_private_threads": user.guild_permissions.create_private_threads,
            	"create_public_threads": user.guild_permissions.create_public_threads,
		"deafen_members": user.guild_permissions.deafen_members,
            	"deafen_members": user.guild_permissions.deafen_members,
            	"embed_links": user.guild_permissions.embed_links,
            	"external_emojis": user.guild_permissions.external_emojis,
            	"external_stickers": user.guild_permissions.external_stickers,
            	"kick_members": user.guild_permissions.kick_members,
            	"manage_channels": user.guild_permissions.manage_channels,
            	"manage_emojis": user.guild_permissions.manage_emojis,
            	"manage_emojis_and_stickers": user.guild_permissions.manage_emojis_and_stickers,
            	"manage_events": user.guild_permissions.manage_events,
            	"manage_guild": user.guild_permissions.manage_guild,
            	"manage_guild_expressions": user.guild_permissions.manage_guild_expressions,
            	"manage_events": user.guild_permissions.manage_events,
            	"manage_messages": user.guild_permissions.manage_messages,
		"manage_nicknames": user.guild_permissions.manage_nicknames,
		"manage_permissions": user.guild_permissions.manage_permissions,
		"manage_roles": user.guild_permissions.manage_roles,
   		"manage_threads": user.guild_permissions.manage_threads,
		"manage_webhooks": user.guild_permissions.manage_webhooks,
		"mention_everyone": user.guild_permissions.mention_everyone,
		"moderate_members": user.guild_permissions.moderate_memberss,
		"move_members": user.guild_permissions.move_members,
		"mute_members": user.guild_permissions.mute_members,
		"priority_speaker": user.guild_permissions.priority_speaker,
		"read_message_history": user.guild_permissions.read_message_history,
		"read_messages": user.guild_permissions.read_messages,
		"request_to_speak": user.guild_permissions.request_to_speak,
		"send_messages": user.guild_permissions.send_messages,
		"send_messages_in_threads": user.guild_permissions.send_messages_in_threads,
		"send_tts_messages": user.guild_permissions.send_tts_messages,
		"send_voice_messages": user.guild_permissions.send_voice_messages,
		"speak": user.guild_permissions.speak,
		"start_embedded_activities": user.guild_permissions.start_embedded_activities,
		"stream": user.guild_permissions.stream,
		"use_application_commands": user.guild_permissions.use_application_commands,
		"use_embedded_activities": user.guild_permissions.use_embedded_activities,
		"use_external_emojis": user.guild_permissions.use_external_emojis,
		"use_external_sounds": user.guild_permissions.use_external_sounds,
		"use_external_stickers": user.guild_permissions.use_external_stickers,
		"use_slash_commands": user.guild_permissions.use_slash_commands,
		"use_soundboard": user.guild_permissions.use_soundboard,
		"use_voice_activation": user.guild_permissions.use_voice_activation,
		"value": user.guild_permissions.value,
		"view_audit_log": user.guild_permissions.view_audit_log,
		"view_channel": user.guild_permissions.view_channel,
		"view_creator_monetization_analytics": user.guild_permissions.view_creator_monetization_analytics,
		"view_guild_insights": user.guild_permissions.view_guild_insights
        }

        return "true" if perms[args_list[2]] else "false"

def setup(handler):
    return Functions(handler)
