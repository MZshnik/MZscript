import asyncio
import os
import importlib.util
import logging

import disnake
from disnake.ext import commands

from .functions_collector import FunctionsCore


class MZClient:
    """
    ## Welcome to MZscript!
    ### This is the main class of MZscript coding. Init this class by typing `MZClient()` and save it to any var like `bot = MZClient()`
    ### You need to use only this methods of class:
    #### `add_command`
    #### `add_slash`
    #### `add_event`
    In rare cases, when your bot very huge, you can use this methods:
    #### `load_command`
    #### `load_commands`
    ### Check [docs](https://mzscript.vercel.app/) and [repository](https://github.com/MZshnik/MZscript) for more information
    """
    def __init__(
        self,
        intents: str = "all",
        on_ready: str = "$console[Bot is ready]",
        db_warns: bool = False,
        debug_log: bool = False,
        debug_console: bool = True,
        ):
        self.user_on_ready = on_ready
        sync_commands = commands.CommandSyncFlags.default()
        sync_commands.sync_commands_debug = debug_log
        self.user_commands = []
        self.user_command_names = []
        self.exec_on_start = []
        self.user_slash_commands = []
        self.user_events = {"message": None, "button": None, "interaction": None}
        self.bot = commands.InteractionBot(
            intents=self._get_intents(intents), command_sync_flags=sync_commands
            )
        self.funcs = FunctionsCore(self, db_warns, debug_log, debug_console)
        self._register_listeners()

    def _get_intents(self, entry: str):
        """
        ## Get intents from provided entry
        """
        if isinstance(entry, disnake.Intents):
            return entry
        elif entry.lower() == "all":
            return disnake.Intents.all()
        elif entry.lower() == "default":
            return disnake.Intents.default()
        else:
            raise ValueError('Intents should be "all" or "default".')

    def _register_listeners(self):
        """
        ## Registers all usedabl events
        """
        self.bot.add_listener(self.on_ready, disnake.Event.ready)
        self.bot.add_listener(self.on_message, disnake.Event.message)
        self.bot.add_listener(self.on_button_click, disnake.Event.button_click)
        self.bot.add_listener(self.on_interaction, disnake.Event.interaction)

    async def update_commands(self):
        """
        ## Update command names which have $function in the name.
        """
        for i in self.exec_on_start:
            self.user_commands[i][0] = await self.funcs.is_have_functions(
                self.user_command_names[i], disnake.Message
            )

    async def run_code(self, code: str, ctx: disnake.Message = None) -> str:
        """
        ## Async run provided code

        ### Args:
            code (`str`): Code with functions (example: `$getVar[prefix]`, `$if[1==1] $text[text1] $else $text[text2] $endif`)
            ctx (`disnake.Message`): Context, default is None

        ### Returns:
            `str`: result of executed functions
        """
        chunks = await self.funcs.get_chunks(code)
        await self.funcs.check_ifs(chunks)
        chunks = await self.funcs.execute_chunks(chunks, ctx)
        return "".join(chunks) if chunks else ""

    def add_command(self, name: str, code: str):
        """
        ## Add command to handlering

        ### Args:
            name (`str`): Trigger what execute command if any person type it in chat. Can execute functions like name of command `$getVar[prefix]help` and finale command name will be view like `!help`
            code (`str`): Code for execute when command invoked. For send message always use $sendMessage - plain text not send. Check docs for info about stable functions.
        """
        self.user_commands.append([name, code])
        self.user_command_names.append(name)
        chunks = asyncio.run(self.funcs.get_chunks(name))
        for chunk in chunks:
            if chunk.startswith("$"):
                self.exec_on_start.append(len(self.user_commands) - 1)

    def add_slash( # TODO: Make full support of slash commands and options
        self, name: str, code: str,
        description: str = None, options: list = None,
        onlyguild: bool = False, isnsfw: bool = False
        ):
        """
        ## Add slash command

        ### Args:
            name (`str`): Equals "name" in add_command, name of slash.
            code (`str`): Code for execute when command invoked.
            description (`str`): Description for slash command.
            options (`list`): List of options in slash command.
            onlyguild (`bool`): Is slash can work only in guild, (by default) False if anywhere.
            isnsfw (`bool`): Is slash can work only in NSFW channels.
        """
        self.bot.add_slash_command(
            commands.InvokableSlashCommand(
                func=self.on_slash, name=name,
                description=description, options=options,
                dm_permission=onlyguild, nsfw=isnsfw,
                auto_sync=True
                )
            )
        self.user_slash_commands.append([name, code])

    def load_command(self, path: str):
        """
        ## Load file with commands

        ### Args:
            path (`str`): Path to file, your example project:\n
                |MyBotDir\n
                |-Cogs\n
                |--mycommands.py\n
                |-main.py\n
                Example load of file mycommands.py:\n
                `bot.load_command("Cogs.mycommand")`
        """
        try:
            spec = importlib.util.find_spec(path)
            lib = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(lib)
            lib.setup(self)
        except ImportError:
            logging.error(f"Cannot import commands from path \"{path}\"")
        except AttributeError:
            logging.error(f"Cannot find setup function for commands in \"{path}\"")

    def load_commands(self, dir: str):
        """
        ## Load directory with commands

        ### Args:
            dir (`str`): Path to dir with commands, your example project:\n
                |MyBotDir\n
                |-CogsDir\n
                |--mycommands.py\n
                |--mycommands1.py\n
                |--ComaSDjs.py\n
                |-main.py\n
                Example load of files in CogsDir directory:\n
                `bot.load_commands("CogsDir")`
        """
        for folder, _, files in os.walk(dir):
            if folder.endswith("__pycache__"):
                continue
            for file in files:
                if file.endswith(".py") and file != "__init__.py":
                    self.load_command(os.path.join(folder, file))

    def add_event(self, name: str, code: str):
        """
        ## Add event code to handlering

        ### Args:
            name (`str`): Event name (like "message"/"button" and etc.). You can see list of all supported events in docs.
            code (`str`): Code for execute when event invoked. For send message always use $sendMessage - plain text not send. Check docs for info about stable functions.
        """
        if name in self.user_events:
            self.user_events[name] = code
        else:
            raise ValueError(f"\"{name}\" event does not exists.")

    async def on_ready(self):
        if self.user_on_ready:
            await self.run_code(self.user_on_ready)
        await self.update_commands()

    async def on_message(self, message: disnake.Message):
        """
        `message` event
        Executed when someone send message(and bots)
        """
        if self.user_events["message"]:
            await self.run_code(self.user_events["message"], message)
        if message.author.bot:
            return
        splitted_command = message.content.split(" ")
        for command_name, command_code in self.user_commands:
            if splitted_command[0] == command_name:
                message.content = " ".join(splitted_command[1:])
                await self.run_code(command_code, message)

    async def on_button_click(self, inter: disnake.MessageInteraction):
        """
        `button` event
        Executed when someone clicked button
        """
        if self.user_events["button"]:
            await self.run_code(self.user_events["button"], inter)

    async def on_interaction(self, inter: disnake.MessageInteraction):
        """
        `interaction` event
        Executed when some of interactions(buttons/menus and etc.) are invoked
        """
        if self.user_events["interaction"]:
            await self.run_code(self.user_events["interaction"], inter)

    async def on_slash(self, inter: disnake.AppCmdInter):
        for name, code in self.user_slash_commands:
            if name == inter.application_command.name:
                await self.run_code(code, inter)

    def run(self, token: str):
        self.bot.run(asyncio.run(self.funcs.is_have_functions(token)))
